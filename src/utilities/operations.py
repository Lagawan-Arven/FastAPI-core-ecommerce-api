from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.utilities.dependecies import get_session
from src.utilities import models
from src.utilities import schemas

#===============================
    #GET PRODUCT BY ID
#===============================
def get_product_by_id(product_id: int,session: Session) -> models.Product:
    
    db_product = session.get(models.Product,product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found!")
    return db_product

#===============================
        #ADD NEW ORDER
#===============================
def add_new_order(user_id: int, order_input: schemas.Base_Order_Create,
                  session: Session) -> models.Order:
    
    #CHECKS IF STOCK IS STILL SUFFICIENT
    item = get_product_by_id(order_input.product_id,session=session)
    if order_input.product_quantity > item.stock:
        raise HTTPException(status_code=400,detail="Insufficient product stock!")

    new_order = models.Order(
        user_id = user_id,
        payment_method = order_input.payment_method,
        payment_status = order_input.payment_status,
        order_products = [models.Order_Product(
                    product_id = order_input.product_id,
                    quantity = order_input.product_quantity)]
    )
       
    item.stock -= order_input.product_quantity

    session.add(new_order)
    session.flush()
    return new_order