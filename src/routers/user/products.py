from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session

from src.database import models
from src.core.dependecies import get_session,pagination_params,get_current_user
from src.core import schemas

router = APIRouter()

#===============================
        #GET ALL PRODUCTS
#===============================
@router.get("/shop/products",response_model= schemas.Paginated_Response[schemas.User_Product_Out])
def get_all_products(pagination = Depends(pagination_params),
                    current_user = Depends(get_current_user),
                    session: Session = Depends(get_session)):
    
    db_products = session.query(models.Product)

    total = db_products.count()
    if not total:
        raise HTTPException(status_code=404,detail="There is no products yet")
    
    products = db_products.offset(pagination["offset"]).limit(pagination["limit"]).all()
    
    return {"total":total,"page":pagination["page"],"limit":pagination["limit"],"items":products}