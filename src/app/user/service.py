from typing import Optional

from src.app.auth.security import get_password_hash, verify_password
from src.app.base.service_base import BaseService
from src.app.base.utils.generate import generate_pass, generate_email
from . import schemas
from .models import User, SocialAccount


class UserService(BaseService):
    model = User
    create_schema = schemas.UserCreateInRegistration
    update_schema = schemas.UserUpdate
    get_schema = schemas.UserGet

    async def create_user(
            self, schema: schemas.UserCreateInRegistration
    ) -> get_schema:
        hash_password = get_password_hash(schema.password)
        return await self.create(
            schemas.UserCreateInRegistration(
                **schema.dict(exclude={"password"}),
                password=hash_password
            )
        )

    async def authenticate(self, username: str, password: str) -> Optional[
        User]:
        obj = await User.get_or_none(username=username)
        if not obj:
            return None
        if not verify_password(password, obj.password):
            return None
        return obj

    async def change_password(self, user: User, new_password):
        hashed_password = get_password_hash(new_password)
        user.password = hashed_password
        await user.save()


user_s = UserService()


async def create_social_account(profile: dict) -> User:
    account = await SocialAccount.get_or_none(account_id=profile['id'])
    if account:
        return account.user
    user = await User.create(
        username=profile['login'],
        first_name=profile['name'],
        avatar=profile['avatar_url'],
        email=generate_email('social_account@mail.ru'),
        password=generate_pass(),
        is_active=True,
    )
    await SocialAccount.create(
        account_id=profile['id'],
        account_url=profile['html_url'],
        account_login=profile['login'],
        account_name=profile['name'],
        provider='github',
        user_id=user.id
    )
    return user
