import os

PROJECT_NAME = "useful"
SERVER_HOST = "http://127.0.0.1:8000"

SECRET_KEY = "HIUHUIGHUIGIUguygfu78hiug78t8g78t78t87t8t8t87t78t878"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_V1_STR = "/api/v1"

# Token 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

# CORS
BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:8080",
]

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "admin123"
POSTGRES_SERVER = "localhost"
POSTGRES_DB = "useful"

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_SERVER}/{POSTGRES_DB}"
)

USERS_OPEN_REGISTRATION = True

SMTP_TLS = True
SMTP_PORT = 587
SMTP_HOST = "smtp.gmail.com"
SMTP_USER = "test@gmail.com"
SMTP_PASSWORD = "joihiuhiu"
EMAILS_FROM_EMAIL = "test@gmail.com"

EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 40
EMAIL_TEMPLATES_DIR = "src/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL
EMAIL_TEST_USER = "test@gmail.com"
