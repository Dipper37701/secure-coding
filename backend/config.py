# backend/config.py
import os

class Config:
    SECRET_KEY = '619dbd528cc746f0fbd0436f348f82b1896218518b632024b04a4bd41fbb53a9'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///marketplace.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend/uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    JWT_SECRET_KEY = 'ac3842678802e9c6b9ab7269c2bc8634a0fd5b7fd7fd0ccf6f4bdc974d16010c'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    REPORT_THRESHOLD_USER = 5  # Number of reports to deactivate a user
    REPORT_THRESHOLD_PRODUCT = 3  # Number of reports to deactivate a product

