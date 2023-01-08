from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.Users import RegisterUser, LoginUser
from mongo import db
from datetime import datetime, timedelta
from models.Token import Token, TokenData
from utils import verify_password
from pathlib import Path
from dotenv import dotenv_values
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
dotenv_path = Path('.env')
config = dotenv_values(dotenv_path)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/register', status_code=status.HTTP_201_CREATED, summary="Register user")
async def register(user: RegisterUser):
    users = db['users']
    new_user = dict(user)
    new_user['registered_at'] = datetime.utcnow()
    result = users.insert_one(new_user)
    return {"user": users.find_one({'_id': result.inserted_id}, {"_id": 0})}


@router.post('/login', summary="Login user")
async def login(data: LoginUser):
    current_user = authenticate_user(data.username, data.password)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config['ACCESS_TOKEN_EXPIRE_MINUTES']))
    access_token = create_access_token(
        data={"sub": current_user['username']}, expires_delta=access_token_expires
    )
    return {"status": 200, "access_token": access_token}


def get_user(username: str):
    users = db['users']
    current_user = users.find_one({"username": username}, {"_id": 0})
    return current_user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config['SECRET_KEY'], algorithms=[config['ALGORITHM']])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config['SECRET_KEY'], algorithm=config['ALGORITHM'])
    return encoded_jwt


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config['ACCESS_TOKEN_EXPIRE_MINUTES']))
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


