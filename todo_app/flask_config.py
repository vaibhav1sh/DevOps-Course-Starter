import os


class Config:
    """Base configuration variables."""
    # SECRET_KEY = "574e0ac08ec210115e288fa9"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
