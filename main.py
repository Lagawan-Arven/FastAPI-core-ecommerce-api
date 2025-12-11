from fastapi import FastAPI,HTTPException,Depends

from sqlalchemy.orm import Session

from database import engine

from database_model import Customer
import database_model

from dependecies import get_session

from models import Customer_Create,Customer_Out

from auth import hash_password,verify_password

app = FastAPI()

database_model.Base.metadata.create_all(bind=engine)

#===============================
        #REGISTER A USER
#===============================
@app.post("/register",response_model=Customer_Out)
def register_user(customer: Customer_Create,
                  session: Session = Depends(get_session)):
    
    #Checks if the customer's account already existed
    db_customer = session.query(Customer).filter(Customer.username==customer.username).first()
    if db_customer:
        raise HTTPException(status_code=400,detail="Account already existed!")
    
    hashed_password = hash_password(customer.password)
    new_customer = Customer(
        name = customer.firstname+" "+customer.lastname,
        age = customer.age,
        sex = customer.sex,
        occupation = customer.occupation,
        username = customer.username,
        password = hashed_password
    )
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer

#===============================
        #LOGI IN USER
#===============================
@app.post("/login")
def login_user(username:str,
               password: str,
               session: Session = Depends(get_session)):
    
    db_customer = session.query(Customer).filter(Customer.username==username).first()
    if not db_customer:
        raise HTTPException(status_code=404,detail="Account did not exist!")
    if not verify_password(password,db_customer.password):
        raise HTTPException(status_code=404,detail="Incorrect password!")

    return {"message":"Log in successful!"}
