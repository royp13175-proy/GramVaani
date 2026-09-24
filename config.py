import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'gramvaani_secret')
    SCHEMES_FILE = 'schemes_data.json'
    SUPPORTED_LANGS = ['hi-IN', 'en-IN', 'en-US']
