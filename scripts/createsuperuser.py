import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
from src.config import settings
from src.app.auth.security import get_password_hash
from src.app.user.models import User
from tortoise import run_async, Tortoise


async def main():
    """ Создание супер юзера """
    await Tortoise.init(
        db_url=settings.DATABASE_URI,
        modules={"models": settings.APPS_MODELS},
    )
    print("Create superuser")
    username = input("Username: ")
    email = input("Email: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    password = input("Password: ")

    user = await User.exists(username=username, email=email)
    if not user:
        await User.create(
            username=username,
            email=email,
            password=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            is_superuser=True,
            is_active=True
        )
        print("Success")
    else:
        print("Error, user existing")


if __name__ == '__main__':
    run_async(main())
