from sqlalchemy.orm import Session

from src.app.base.utils.generate import generate_pass, generate_email
from . import schemas, crud
from .models import User


def create_social_account(db: Session, profile: dict) -> User:
    if crud.social_account.exists(db, account_id=profile['id']):
        account = crud.social_account.get(db, account_id=profile['id'])
        return account.user
    account = schemas.SocialAccount(
        account_id=profile['id'],
        account_url=profile['html_url'],
        account_login=profile['login'],
        account_name=profile['name'],
        provider='github',
    )
    user = schemas.UserCreate(
        username=profile['login'],
        first_name=profile['name'],
        avatar=profile['avatar_url'],
        email=generate_email('social_account@mail.ru'),
        password=generate_pass(),
        is_active=True,
    )
    user_obj = crud.user.create(db, schema=user)
    crud.social_account.create(db, schema=account, user_id=user_obj.id)
    return user_obj
