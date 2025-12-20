from fastapi import FastAPI,HTTPException,Depends,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import models
from app.dependecies import get_session
from app import schemas 
from app.auth import hash_password,verify_password,create_access_token

router = APIRouter()

#===============================
        #REGISTER AN ADMIN
#===============================
@router.post("/register/admin")
def register_admin(session: Session = Depends(get_session)):
    
    #Checks if the customer's account already existed
    db_user = session.query(models.User).filter(models.User.username=="admin").first()
    if db_user:
        raise HTTPException(status_code=400,detail="Account already exist!")
    
    hashed_password = hash_password("1234")
    new_user = models.User(
        fullname = "admin",
        age = 0,
        gender = "admin",
        occupation = "admin",
        username = "admin",
        email = "admin",
        password = hashed_password,
        role = "admin"
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

#===============================
        #REGISTER A USER
#===============================
@router.post("/register",response_model=schemas.Base_User_Out)
def register_user(user_data: schemas.User_Create,
                  session: Session = Depends(get_session)):
    
    #Checks if the customer's account already existed
    db_user = session.query(models.User).filter(models.User.username==user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400,detail="Account already exist!")
    
    hashed_password = hash_password(user_data.password)
    new_user = models.User(
        fullname = user_data.firstname.capitalize() +" "+ user_data.lastname.capitalize(),
        age = user_data.age,
        gender = user_data.gender.capitalize(),
        occupation = user_data.occupation.capitalize(),
        username = user_data.username,
        email = user_data.email,
        password = hashed_password
    )
    new_user.cart = models.Cart(user = new_user)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

#===============================
        #LOG IN USER
#===============================
@router.post("/login")
def login_user(username:str,
               password: str,
               session: Session = Depends(get_session)):
    
    db_user = session.query(models.User).filter(models.User.username==username).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="Account not found!")
    
    if not verify_password(password,db_user.password):
        raise HTTPException(status_code=400,detail="Incorrect password!")
    
    token = create_access_token({"id":db_user.id,"role":db_user.role})

    return {"message":"Log in successful!","access_token":token,"token_type":"bearer"}

@router.post("/login_test")
def login_user(data_form: OAuth2PasswordRequestForm = Depends(),
               session: Session = Depends(get_session)):
    
    db_user = session.query(models.User).filter(models.User.username==data_form.username).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="Account not found!")
    
    if not verify_password(data_form.password,db_user.password):
        raise HTTPException(status_code=400,detail="Incorrect password!")
    
    token = create_access_token({"id":db_user.id,"role":db_user.role})

    return {"message":"Log in successful!","access_token":token,"token_type":"bearer"}