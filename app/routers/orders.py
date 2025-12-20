from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session

from app import schemas
from app.dependecies import get_current_user,get_session,admin_access
from app.database import models

router = APIRouter()

@router.post("/orders",response_model=schemas.Base_Order_Out)
def add_order(order_input: schemas.Base_Order_Create,
              current_user = Depends(get_current_user),
              session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=401,detail="User not logged in!")
    
    db_product = session.get(models.Product,order_input.product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    if db_product.stock < order_input.product_quantity:
        raise HTTPException(status_code=400,detail="Insufficient product stock!")

    new_order = models.Order(
        user_id = db_user.id,
        payment_method = order_input.payment_method,
        payment_status = order_input.payment_status
    )
    new_order.order_products =[ models.Order_Product(
        product_id = db_product.id,
        quantity = order_input.product_quantity
    )]

    db_product.stock -= order_input.product_quantity

    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

@router.get("/orders",response_model=list[schemas.Base_Order_Out])
def get_all_orders(current_user = Depends(admin_access),
               session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=401,detail="User not logged in!")
    
    db_orders = session.query(models.Order).all()
    if not db_orders:
        raise HTTPException(status_code=401,detail="There is no order yet!")
    
    return db_orders