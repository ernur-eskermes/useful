from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from tortoise.contrib.fastapi import register_tortoise

from src.app import routers
from src.config import settings

app = FastAPI(
    title='Useful',
    description='Useful',
    version='0.1.0'
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app=app,
    db_url=settings.DATABASE_URI,
    modules={
        "models": settings.APPS_MODELS
    },
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(routers.api_router, prefix=settings.API_V1_STR)
