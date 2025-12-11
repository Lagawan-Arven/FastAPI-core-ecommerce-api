from pydantic import BaseModel

class Customer_Personal_Info(BaseModel):
    age: int
    firstname: str
    lastname: str
    sex: str
    occupation: str

class Customer_Create(Customer_Personal_Info):
    username: str
    password: str

class Customer_Out(BaseModel):
    username: str
    
    class Config:
        from_attributes = True

