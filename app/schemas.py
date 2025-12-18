from pydantic import BaseModel
from typing import Optional

#===================================
                #USERS
#===================================
class User_Personal_Info(BaseModel):
    age: int
    gender: str
    occupation: str

class User_Login_Credential(BaseModel):
    username: str
    email: str

class Base_User(User_Personal_Info,User_Login_Credential):
    pass

class User_Create(Base_User):
    firstname: str
    lastname: str
    password: str

class User_Update(User_Personal_Info):
    firstname: str
    lastname: str

class User_Credential_Update(User_Login_Credential):
    password: str

class Base_User_Out(Base_User):
    id: str
    fullname: str

    class Config:
        from_attributes = True

class User_Out(BaseModel):
    id: str
    username: str
    cart: Cart_Out

#===================================
                #CARTS
#===================================
class Cart_Out(BaseModel):
    orders: list[str] = []

    class Config:
        from_attributes = True

#===================================
                #ORDERS
#===================================
class Base_Order(BaseModel):
    id: str
    cart_id: str
    status: str
    payment_method: str
    payment_status: str

class Order_Create():
    pass
    
class Base_Order_Out(Base_Order):
    products: list[str] = []

    class Config:
        from_attributes = True

#===================================
        #ODER-PRODUCT LINK
#===================================

#===================================
                #PRODUCTS
#===================================
class Base_Product(BaseModel):
    name: str
    details: Optional[object] = None
    price: float
    stock: int

class Product_Create(Base_Product):
    pass

class Product_Update(Base_Product):
    pass

class Base_Product_Out(Base_Product):
    id: str
    orders: list[str] = []

    class Config:
        from_attributes = True

class Product_Out(BaseModel):
    id: str
    name: str
    details: Optional[object] = None
    price: float

    class Config:
        from_attributes = True

