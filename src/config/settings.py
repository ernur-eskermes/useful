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

DATABASE_URI = (
    f"postgres://{os.environ.get('POSTGRES_USER')}:"
    f"{os.environ.get('POSTGRES_PASSWORD')}@"
    f"{os.environ.get('POSTGRES_HOST')}/"
    f"{os.environ.get('POSTGRES_DB')}"
)

APPS_MODELS = [
    "src.app.user.models",
    "src.app.auth.models",
    "src.app.board.models",
    "aerich.models",
]

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URI},
    "apps": {
        "models": {
            "models": APPS_MODELS,
            "default_connection": "default",
        },
    },
}

USERS_OPEN_REGISTRATION = True

SMTP_TLS = os.environ.get("SMTP_TLS")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = os.environ.get("EMAILS_FROM_EMAIL")

EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 40
EMAIL_TEMPLATES_DIR = "src/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL

GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")
