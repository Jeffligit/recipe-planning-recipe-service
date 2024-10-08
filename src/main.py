from typing import Annotated, Optional
import os

from .auth.user_auth import create_access_token, decode_access_token, verify_password, create_access_cookie
from .database import SessionLocal, engine
from .models import Base
from .schemas import Recipe, RecipeCreate, User, UserCreate, TokenData, Token, Ingredient, Macro, MacroCreate, Mealplan
from .user.crud import create_user, get_user_by_username, get_user_by_email, get_user
from .recipe.crud import create_recipe, get_recipe
from .ingredient.crud import create_ingredient
from .macro.crud import create_macro, get_macro_from_recipe, get_macro
from .mealplan.crud import create_mealplan, get_mealplan
from .meal.crud import create_meal

from fastapi import Depends, FastAPI, HTTPException, status, Response, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError 
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import date

load_dotenv()
Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    os.getenv("CORS_ORIGIN")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    '''
    Checks if the service is healthy
    '''
    return ""


def verify_jwt(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    '''
    Verifies the JWT (JSON Web Token)

    Paramater: 
        token: a JWT token supplied in the header of the request

    Return: TokenData object
    '''
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
    

def get_auth_cookie(jwt: Annotated[str | None, Cookie()] = None) -> dict:
    if jwt is None:
        raise HTTPException(status_code=403, detail="Token not provided")
    return verify_jwt(jwt)


@app.post('/signup')
def signup(response: Response, user: UserCreate, db: Session = Depends(get_db)):
    '''
    Creates a user in the database

     Parameters: 
        user: UserCreate object in the response body
        db: database session

    Returns: response_model=User json of User schema
    '''
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is in use")

    createdUser = create_user(db, user)
    create_access_cookie(response=response, email=createdUser.email, id=createdUser.id)
    return {"user_id": createdUser.id}
    

@app.post('/token')
def login_for_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    '''
    Verifies login credentials from from received in the header. Creates a jwt token from the information provided

    Parameter:
        form_data: login credentials provided in the header.
        db: db session
    Returns: 
        Token: jwt token object
    '''
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    create_access_cookie(response=response, email=user.email, id=user.id)
    return { "user_id": user.id }
    
    
@app.get('/user', response_model=User)
def read_user(token_data: Annotated[TokenData, Depends(get_auth_cookie)], db: Session = Depends(get_db)):
    '''
    Retrieves user using information provided in the JWT token

    Parameters: 
        token_data: TokenData object created from verifying the jwt token. Has a dependency function verify_wt
        db: database session

    Returns: response_model=User json of User schema
    '''
    user = get_user(db, user_id=token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post('/recipe', response_model=Recipe)
def add_recipe(token_data: Annotated[TokenData, Depends(verify_jwt)], recipe: RecipeCreate, db: Annotated[Session, Depends(get_db)]):
    '''
    Add Recipe to DB

    Parameters:
        token_data: TokenData object created from verifying the jwt token. We want to use the 'user_id' found here.
        recipe: RecipeCreate object. Contains information needed for creating a recipe in the database.
        db: db session

    Returns:
        Recipe Object
    '''

    return create_recipe(db=db, recipe=recipe, user_id=token_data.user_id)

@app.get('/recipe', response_model=Recipe)
def read_recipe(db: Annotated[Session, Depends(get_db)], recipe_id: int):
    '''
    Get Recipe from DB by id

    Parameters:
        db: db session
        recipe_id: id of recipe

    Returns:
        Recipe Object
    '''

    return get_recipe(db, recipe_id)

@app.get('/ingredient', response_model=Ingredient)
def add_ingredient(db: Annotated[Session, Depends(get_db)], id: int, name: str):
    '''
    For Testing Purposes

    Add Ingredient
    '''

    return create_ingredient(db, id, name)

@app.post('/macro', response_model=Macro)
def add_macro(db: Annotated[Session, Depends(get_db)], macro: MacroCreate, recipe_id: int, token_data: Annotated[TokenData, Depends(verify_jwt)]):
    '''
    For Testing Purposes

    Add Macro
    '''
    return create_macro(db, macro, recipe_id)

@app.get('/macro', response_model=Macro)
def read_macro(db: Annotated[Session, Depends(get_db)], macro_id: int):
    '''
    Get Macro from Macro ID
    '''
    
    return get_macro(db, macro_id)


@app.get('/macro/from-recipe', response_model=Macro)
def read_macro_from_recipe(db: Annotated[Session, Depends(get_db)], recipe_id: int):
    '''
    Get Macro from Recipe ID
    '''

    return get_macro_from_recipe(db, recipe_id)

@app.get('/get_cookie_info')
def get_cookie_info(token_data: Annotated[TokenData, Depends(get_auth_cookie)]):
    '''
    Get information encrypted inside the cookie set for with authed.
    '''
    return token_data

@app.post('/mealplan', response_model=Mealplan)
def add_mealplan(db: Annotated[Session, Depends(get_db)], token_data: Annotated[TokenData, Depends(verify_jwt)], title: str, days: list[object]):
    mealplan = create_mealplan(db, user_id=1, title=title, createdOn=date.now(), lastUpdated=date.now())

    for day in days:
        create_meal(db, mealplan.id, day.get("recipe"), day.get("servings"), day.get("date"))

    return mealplan

@app.get('/mealplan', response_model=Mealplan)
def read_mealplan(db: Annotated[Session, Depends(get_db)], mealplan_id: int):
    '''
    Get Mealplan from Mealplan ID
    '''

    return get_mealplan(db=db, mealplan_id=mealplan_id)
