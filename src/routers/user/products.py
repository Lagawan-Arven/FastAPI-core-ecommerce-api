from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from redis.asyncio import Redis
import json

from src.utilities import models
from src.utilities.dependecies import get_session,pagination_params,get_current_user,get_redis
from src.utilities import schemas

router = APIRouter()

#===============================
        #GET ALL PRODUCTS
#===============================
@router.get("/shop/products",response_model= schemas.Paginated_Response[schemas.User_Product_Out])
async def get_all_products(pagination = Depends(pagination_params),
                    current_user = Depends(get_current_user),
                    session: Session = Depends(get_session),
                    redis: Redis = Depends(get_redis)):
    
    page = pagination["page"]
    limit = pagination["limit"]
    offset = pagination["offset"]

    cached_key = f"products: page={page},limit={limit}"
    cached_data = await redis.get(cached_key)
    if cached_data:
        return json.loads(cached_data)

    db_products = session.query(models.Product)

    total = db_products.count()
    if not total:
        raise HTTPException(status_code=404,detail="There is no products yet")
    
    products = db_products.offset(offset).limit(limit).all()

    items = [schemas.User_Product_Out.model_validate(product).model_dump() for product in products]

    response = {
        "total":total,
        "page" :page,
        "limit":limit,
        "items":items
    }

    await redis.setex(
        cached_key,
        300,
        json.dumps(response,default=str),
    )
    
    return response