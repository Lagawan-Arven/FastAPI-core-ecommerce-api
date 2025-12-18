from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session

from app import schemas
from app.dependecies import get_current_user,get_session
from app.database import models

router = APIRouter

@router.post("/orders",response_model=schemas.Base_Order_Out)
def add_order(order_input: Order_Create,
              product_id: str,
              current_user = Depends(get_current_user),
              session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=401,detail="User not logged in!")
    
    db_products = session.query(PRODUCT).filter(PRODUCT.id.in_(product_id_list.ids)).all()
    if not db_products:
        return {"message":"Products not found!"}
    order_input.products = db_products

    new_order = models.Order(
        
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

@router.get("/orders",response_model=Order_Out)
def get_orders(current_user = Depends(get_current_user),
               session: Session = Depends(get_session)):
    
    db_customer = session.query(CUSTOMER).filter(CUSTOMER.id==current_user.id).first()
    if not db_customer:
        return {"message":"User not logged in!"}
    
    db_orders = session.query(ORDER).filter(ORDER.customer_id==db_customer.id).all()
    if db_orders == []:
        return {"message":"There is no order for this account yet!"}
    
    return db_orders