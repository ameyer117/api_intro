from datetime import timedelta

from fastapi import Depends, HTTPException, APIRouter
from starlette import status

from crud.user import authenticate_user, create_access_token, get_current_user, get_user, get_password_hash, insert_user
from schemas.user import User, UserInDB, Token, CreateUserRequest, LoginUserRequest

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/token", response_model=Token, description="Get a JWT Bearer token for authentication")
async def login_for_access_token(login_request: LoginUserRequest):
    user = authenticate_user(login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=User)
async def create_user(user: CreateUserRequest):
    # Check if user already exists
    if get_user(user.email):
        raise HTTPException(
            status_code=400,
            detail="User with email already registered"
        )
    # Hash the password
    hashed_password = get_password_hash(user.password)
    # Create new user document
    insert_user(UserInDB(email=user.email, full_name=user.full_name, hashed_password=hashed_password))
    # Return the created user
    return user