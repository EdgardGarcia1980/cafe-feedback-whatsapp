import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

    # MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI')
    MONGODB_DB_NAME = 'cafe_feedback'
    MONGODB_COLLECTION = 'mensajes'

    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Flask
    PORT = int(os.getenv('PORT', 5000))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
