import os
from flask import Flask, request, Response, abort
from functools import wraps
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

load_dotenv()

app = Flask(__name__)

auth_token = os.getenv("TWILIO_AUTH_TOKEN")
webhook_url = os.getenv("WEBHOOK_URL")


# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="meta-llama/llama-4-maverick-17b-128e-instruct"  # or "mixtral-8x7b-32768"
)

# Define prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. please reply in less than 1500 characters"),
    ("user", "{input}")
])

# Build expressive chain
chain = (
    {"input": RunnablePassthrough()}
    | prompt
    | llm
    | RunnableLambda(lambda output: output.content)
)


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(auth_token)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            webhook_url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function


@app.route("/twilio-webhook", methods=["POST"])
@validate_twilio_request
def twilio_webhook():
    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")

    # Run LangChain pipeline
    groq_reply = chain.invoke(incoming_msg)

    # Respond via Twilio
    resp = MessagingResponse()
    resp.message(groq_reply)

    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(debug=True)