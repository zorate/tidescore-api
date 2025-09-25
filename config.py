import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/tidescore')
    DATABASE_NAME = 'tidescore'
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # API
    API_VERSION = 'v1'
    SCORE_CACHE_DAYS = 30
    MAX_API_REQUESTS_PER_MINUTE = 100
    
    # Security
    BCROUNDS = 12