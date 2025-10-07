# Minimalist Whatsapp LLM Chatbot 
Simple Implementation of Whatsapp based LLM chatbot - Whatspp <-> Twilio <-> Python Backend <-> LLM

# Installation Steps

## Step 1: Create Account on Twilio Console
- Sign up or log in to the Twilio Console.
- Obtain your **Auth Token**.

## Step 2: Get Groq API Key
- Register or log in to Groq.
- Obtain your **API Key**.

## Step 3: Configure Port Forwarding in Visual Studio Code for Port 5000
- Go to the **PORTS** tab in VS Code.
- Set up port forwarding for port `5000`.
- **Copy the Webhook URL** shown in the PORTS tab.

## Step 4: Installation

1. **Create a virtual environment:**
```
python3 -m venv venv
```
2. **Activate the virtual environment:**
- On Linux/macOS:
  ```
  source venv/bin/activate
  ```
- On Windows:
  ```
  venv\Scripts\activate
  ```
3. **Install dependencies:**
```
pip install -r requirements.txt
```
4. **Set up environment variables:**
- Copy `.env.example` to `.env`
- Update `.env` with your **Twilio Auth Token**, **Groq API key**, and **Webhook URL**

## Step 5: Run the Application
```
python app.py
```
