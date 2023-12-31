

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///tktshowdb.sqlite3"
    DEBUG = True
    SECRET_KEY =  "ash ah secet"
    SECURITY_PASSWORD_HASH = "bcrypt"    
    SECURITY_PASSWORD_SALT = "really super secret" # Read from ENV in your case
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False

    #celery config
    REDIS_URL = "redis://localhost:6379"
    CELERY_BROKER_URL="redis://localhost:6379"
    CELERY_RESULT_BACKEND= "redis://localhost:6379"
    ENABLE_UTC = False
    TIMEZONE = "Asia/Calcutta"