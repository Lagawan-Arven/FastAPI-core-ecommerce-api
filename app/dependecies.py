from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from jose import jwt

from app.database.database import local_session
from app.database import models
from app.auth import SECRET_KEY,ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_test")

def get_session():
    session = local_session()
    try:
        yield session
    finally:
        session.close()

def get_current_user(token: str =  Depends(oauth2_scheme),
                     session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = int(payload.get("id"))
    except:
        raise HTTPException(status_code=400,detail="Invalid token!")
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    return db_user

def admin_access(current_user = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Access denied")
    
    return current_user