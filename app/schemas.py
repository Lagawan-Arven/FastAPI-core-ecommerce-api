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

class Base_User_Out(Base_User):
    id: int
    fullname: str
    cart: Cart_Out
    orders: list[Order_Out] = []

    class Config:
        from_attributes = True

class User_Out(BaseModel):
    id: int
    username: str
    cart: Cart_Out
    orders: list[Order_Out] = []

#===================================
                #CARTS
#===================================
class Base_Cart_Out(BaseModel):
    user_id: int
    cart_products: list[Cart_Product_Out] = []

    class Config:
        from_attributes = True

class Cart_Out(BaseModel):
    cart_products: list[Cart_Product_Out] = []

    class Config:
        from_attributes = True


#===================================
        #CART-PRODUCT LINK
#===================================
class Cart_Product_Out(BaseModel):
    product: Product_Out
    quantity: int

    class Config:
        from_attributes = True

class Product_Cart_Out(BaseModel):
    cart_id: int

    class Config:
        from_attributes = True

#===================================
                #ORDERS
#===================================
class Base_Order(BaseModel):
    payment_method: str
    payment_status: str

class Order_Create(Base_Order):
    pass

class Base_Order_Create(Base_Order):
    product_id: int
    product_quantity: Optional[int] = 1
    
class Base_Order_Out(Base_Order):
    user_id: int
    id: int
    status: str
    order_products: list[Order_Product_Out] = []

    class Config:
        from_attributes = True

class Order_Out(Base_Order):
    id: int
    status: str
    order_products: list[Order_Product_Out] = []

    class Config:
        from_attributes = True


#===================================
        #ODER-PRODUCT LINK
#===================================
class Order_Product_Out(BaseModel):
    product: Product_Out
    quantity: int

    class Config:
        from_attributes = True


class Product_Order_Out(BaseModel):
    order_id: int

    class Config:
        from_attributes = True

#===================================
                #PRODUCTS
#===================================
class Base_Product(BaseModel):
    name: str
    price: float
    stock: int

class Product_Create(Base_Product):
    pass

class Product_Update(Base_Product):
    pass

class Base_Product_Out(Base_Product):
    id: int
    product_carts: list[Product_Cart_Out] = []
    product_orders: list[Product_Order_Out] = []

    class Config:
        from_attributes = True

class Product_Out(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

