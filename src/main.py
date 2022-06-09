import re
from datetime import timedelta

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from src.db import models
from src.db.database import get_db, engine
from src.db.services import get_user_by_email, create_user
from src.schemas import Token, User, UserCreate
from src.services import authenticate_user, create_access_token


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.post("/token", response_model=Token)
async def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    request.session["access_token"] = access_token
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registration endpoint. Content can be sent as a json in body.
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # can contain uppercase, lowercase, numbers, special symbols
    if not re.fullmatch(r'[A-Za-z0-9!@#$%^&*()_\-+={\[}\]|\\:;"\'<,>.?]{8,}', user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password can only contain uppercase, lowercase letters, numbers and special symbols",
        )
    return create_user(db, user)


