from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.dependecies import get_current_user,get_session,admin_access
from app.database import models
from app import schemas

router = APIRouter()

#===============================
        #GET ALL USERS
#===============================
@router.get("/users",response_model=list[schemas.Base_User_Out])
def get_all_users(user = Depends(admin_access),
                  session: Session = Depends(get_session)):

    current_user = session.get(models.User,user.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_users = session.query(models.User).all()
    if not db_users:
        raise HTTPException(status_code=404,detail="There is no users yet!")
    
    return db_users

#===============================
        #GET A USER
#===============================
@router.get("/user",response_model=schemas.Base_User_Out)
def get_user_by_id(user = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    
    current_user = session.get(models.User,user.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    return current_user

@router.get("/user/{user_id}",response_model=schemas.Base_User_Out)
def get_user_by_id(user_id: int, user = Depends(admin_access),
                   session: Session = Depends(get_session)):
    
    current_user = session.get(models.User,user.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    return current_user

#===============================
        #RESTRICT A USER
#===============================
'''@router.post("/users/{user_id}")
def restrict_user(user_id: int, user = Depends(admin_access),
                  session: Session = Depends(get_session)):

    current_user = session.get(models.User,user.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    return'''

#===============================
        #DELETE A USER
#===============================
@router.delete("/users/{user_id}")
def delete_user(user_id: int, user = Depends(admin_access),session: Session = Depends(get_session)):

    current_user = session.get(models.User,user.id)
    if not current_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    session.delete(db_user)
    session.commit()
    return {"message":"User deleted successfully!"}