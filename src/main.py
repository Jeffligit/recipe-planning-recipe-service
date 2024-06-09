from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError 
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine
from typing import Annotated
from .schemas import User, UserCreate, TokenData, Token
from .auth.user_auth import create_access_token, decode_access_token, verify_password
from .user.crud import create_user, get_user_by_username, get_user_by_email, get_user
 

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def root():
    return "Hello World"

@app.get('/health')
def health():
    return ""

def verify_jwt(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(
            email=email,
            user_id=payload.get("user_id")
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired",
            headers={"WWW-Authenticate": "Bearer"},
        )    
    except InvalidTokenError:
        raise credentials_exception
    
@app.get('/user/', response_model=User)
def read_user(token_data: Annotated[TokenData, Depends(verify_jwt)], db: Session = Depends(get_db)):
    user = get_user(db, user_id=token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post('/token')
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    # log in with email
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({ "sub": user.email, "user_id": user.id })

    return Token(access_token=access_token, token_type="bearer")


@app.post('/signup', response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # check if email is in use
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is in use")

    return create_user(db, user)
