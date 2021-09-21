from fastapi import APIRouter, Depends, HTTPException, Body, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from src.app.user import schemas, service
from src.app.user.models import User
from src.config.social_app import oauth
from .jwt import create_access_token
from .schemas import Token, Msg, VerificationInDB
from .send_email import send_reset_password_email
from .service import (
    registration_user,
    verify_registration_user,
    generate_password_reset_token,
    verify_password_reset_token,
)

auth_router = APIRouter()


@auth_router.get('/github-login')
async def login_oauth(request: Request):
    github = oauth.create_client("github")
    redirect_uri = request.url_for("authorize_github")
    return await github.authorize_redirect(request, redirect_uri)


@auth_router.get('/github-auth')
async def authorize_github(request: Request):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get("user", token=token)
    user = await service.create_social_account(
        profile=resp.json()
    )
    return create_access_token(data={"user_id": user.id})


@auth_router.post('/login/access-token', response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await service.user_s.authenticate(
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return create_access_token(data={"user_id": user.id})


@auth_router.post("/registration", response_model=Msg)
async def user_registration(
        new_user: schemas.UserCreateInRegistration,
        task: BackgroundTasks
):
    user_exists = await registration_user(new_user, task=task)
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"msg": "Send email"}


@auth_router.post("/confirm-email", response_model=Msg)
async def confirm_email(uuid: VerificationInDB):
    if not await verify_registration_user(uuid):
        raise HTTPException(status_code=404, detail="Not found")
    return {"msg": "Success verify email"}


@auth_router.post("/password-recovery/{email}", response_model=Msg)
async def recover_password(email: str, task: BackgroundTasks):
    user = await User.get_or_none(email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    task.add_task(
        send_reset_password_email,
        email_to=user.email,
        email=email,
        token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@auth_router.post("/reset-password/", response_model=Msg)
async def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
):
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    await service.user_s.change_password(
        user=user,
        new_password=new_password
    )
    return {"msg": "Password updated successfully"}
