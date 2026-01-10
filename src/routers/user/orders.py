import logging
from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session

from src.utilities import schemas
from src.utilities.dependecies import pagination_params,get_session,get_current_user
from src.utilities import models
from src.utilities import operations

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

#===============================
        #GET ALL ORDERS
#==============================
@router.get("/orders",response_model=schemas.Paginated_Response[schemas.Base_Order_Out])
def get_all_orders( pagination = Depends(pagination_params),
                   current_user = Depends(get_current_user),
                    session: Session = Depends(get_session)):
    
    db_orders = session.query(models.Order).filter(models.Order.user_id==current_user.id)

    total = db_orders.count()
    if not total:
        raise HTTPException(status_code=404,detail="There is no order yet!")
    
    orders = db_orders.limit(pagination["limit"]).offset(pagination["offset"]).all()
    
    return {"total":total,"page":pagination["page"],"limit":pagination["limit"],"items":orders}

#===============================
            #ADD ORDER
#===============================
@router.post("/orders",response_model=schemas.Base_Order_Out)
def add_order(order_input: schemas.Base_Order_Create,
              current_user = Depends(get_current_user),
              session: Session = Depends(get_session)):
    
    try:
        new_order = operations.add_new_order(user_id=current_user.id,order_input=order_input,session=session)

        session.commit()
        session.refresh(new_order)
        logger.info("Adding an order successfull")
        return new_order
    
    except HTTPException:
        session.rollback()
        logger.info("HTTPException | Adding an order failed")
        raise

    except Exception as e:
        session.rollback()
        logger.info("500 Internal Server Error | Adding an order failed")
        raise HTTPException(status_code=500,detail="Checkout failed") from e