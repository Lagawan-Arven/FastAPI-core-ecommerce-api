from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,Query,Request
from redis.asyncio import Redis
from sqlalchemy.orm import Session
from jose import jwt

from src.configurations.database import local_session
from src.utilities import models
from src.utilities.auth import SECRET_KEY,ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login_test")

def get_session():
    session = local_session()
    try:
        yield session
    finally:
        session.close()

def get_redis(request: Request) -> Redis:
    if not request.app.state.redis:
        raise HTTPException(status_code=400,detail="Redis is not initialized")
    return request.app.state.redis

def get_current_user(token: str =  Depends(oauth2_scheme),
                     session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = int(payload.get("id"))
    except:
        raise HTTPException(status_code=400,detail="Invalid token!")
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    return db_user

def get_admin_access(current_user = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Access denied")
    
    return current_user

def pagination_params(page: int = Query(1,ge=1),limit: int = Query(10,ge=1,le=100)):

    offset = (page - 1)*limit
    return {"page":page,"limit":limit,"offset":offset}