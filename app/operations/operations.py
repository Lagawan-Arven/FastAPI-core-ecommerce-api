from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session

from app.dependecies import get_session
from app.database import models
from app import schemas
from app.operations import operations

#===============================
    #GET PRODUCT BY ID
#===============================
def get_product_by_id(product_id,session: Session = Depends(get_session)):
    
    db_product = session.get(models.Product,product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found!")
    return db_product

#===============================
        #ADD NEW ORDER
#===============================
def add_new_order(user_id, order_input: schemas.Base_Order_Create,
                  session: Session = Depends(get_session)):
    
    #CHECKS IF STOCK IS STILL SUFFICIENT
    item = operations.get_product_by_id(order_input.product_id)
    if order_input.quantity > item.stock:
        raise HTTPException(status_code=400,detail="Insufficient product stock!")

    new_order = models.Order(
        user_id = user_id,
        payment_method = order_input.payment_method,
        payment_status = order_input.payment_status
    )
    new_order.order_products = [models.Order_Product(
                        product_id = order_input.product_id,
                        quantity = order_input.product_quantity)]
    
    item.stock -= order_input.product_quantity

    session.add(new_order)
    session.flush()
    return new_order