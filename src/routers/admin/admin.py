from fastapi import APIRouter,HTTPException,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.dependecies import get_session,pagination_params,get_admin_access
from src.database import models
from src.core import schemas
from src.operations import operations

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

#======================================================================
                            #USERS
#======================================================================
#===============================
        #GET ALL USERS
#===============================
@router.get("/users",response_model=schemas.Paginated_Response[schemas.Base_User_Out])
def get_all_users(pagination = Depends(pagination_params),
                  admin_access = Depends(get_admin_access),
                  session: Session = Depends(get_session)):

    db_users = session.query(models.User)

    total = db_users.count()
    if not total:
        raise HTTPException(status_code=404,detail="There is no users yet!")
    
    users = db_users.limit(pagination["limit"]).offset(pagination["offset"]).all()
    
    return {"total":total,"page":pagination["page"],"limit":pagination["limit"],"items":users}

#===============================
        #GET USER BY ID
#===============================
@router.get("/users/{user_id}",response_model=schemas.Base_User_Out)
def get_user_by_id(user_id: int, 
                   admin_access = Depends(get_admin_access),
                   session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    return db_user

#===============================
        #DELETE A USER
#===============================
@router.delete("/users/{user_id}")
def delete_user(user_id: int,
                admin_access = Depends(get_admin_access),
                session: Session = Depends(get_session)) -> JSONResponse:
    
    db_user = session.get(models.User,user_id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    session.delete(db_user)
    session.commit()

    logger.info("Admin deleted a user |deleted user_id: %s | admin_id: %s",db_user.id,admin_access.id)
    return {"message":"User deleted successfully!"}

#======================================================================
                            #ORDERS
#======================================================================
#===============================
        #GET ALL ORDERS
#==============================
@router.get("/orders",response_model=schemas.Paginated_Response[schemas.Base_Order_Out])
def get_all_orders(pagination = Depends(pagination_params),
                   admin_access = Depends(get_admin_access),
                   session: Session = Depends(get_session)):
    
    db_orders = session.query(models.Order)

    total = db_orders.count()
    if not total:
        raise HTTPException(status_code=404,detail="There is no order yet!")
    
    orders = db_orders.limit(pagination["limit"]).offset(pagination["offset"]).all()
    
    return {"total":total,"page":pagination["page"],"limit":pagination["limit"],"items":orders}

#======================================================================
                            #PRODUCTS
#======================================================================
#===============================
        #GET ALL PRODUCTS
#===============================
@router.get("/products",response_model= schemas.Paginated_Response[schemas.Base_Product_Out])
def get_all_products(pagination = Depends(pagination_params),
                     admin_access = Depends(get_admin_access),
                    session: Session = Depends(get_session)):
    
    db_products = session.query(models.Product)
        
    total = db_products.count()
    if not total:
        raise HTTPException(status_code=404,detail="There is no products yet")
    
    products = db_products.offset(pagination["offset"]).limit(pagination["limit"]).all()
    
    return {"total":total,"page":pagination["page"],"limit":pagination["limit"],"items":products}

#===============================
        #GET PRODUCT BY ID
#===============================
@router.get("/products/{product_id}",response_model=schemas.Base_Product_Out)
def get_product_by_id(product_id: int,
                      admin_access = Depends(get_admin_access),
                      session: Session = Depends(get_session)):
    
    db_product = operations.get_product_by_id(product_id,session)
    return db_product

#===============================
        #ADD A PRODUCT
#===============================
@router.post("/products",response_model=schemas.Base_Product_Out)
def add_prodcuct(product_input: schemas.Product_Create,
                 admin_access = Depends(get_admin_access),
                 session: Session = Depends(get_session)):
    
    new_product = models.Product(
        name = product_input.name,
        stock = product_input.stock,
        price = product_input.price,
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    logger.info("Admin added a product | admin_id: %s",admin_access.id)

    return new_product

#===============================
        #UPDATE A PRODUCT
#===============================
@router.put("/products/{product_id}",response_model=schemas.Base_Product_Out)
def update_product(product_id: int, product_updates: schemas.Product_Update,
                    admin_access = Depends(get_admin_access),
                    session: Session = Depends(get_session)):
    
    db_product = operations.get_product_by_id(product_id,session)
    
    db_product.name = product_updates.name
    db_product.price = product_updates.price
    db_product.stock = product_updates.stock

    session.commit()
    session.refresh(db_product)

    logger.info("Admin updated a product | admin_id: %s",admin_access.id)

    return db_product

#===============================
        #DELETE A PRODUCT
#===============================
@router.delete("/products/{product_id}")
def delete_product(product_id: int,
                    admin_access = Depends(get_admin_access),
                    session: Session = Depends(get_session)):
    
    db_product = operations.get_product_by_id(product_id,session)
    
    session.delete(db_product)
    session.commit()

    logger.info("Admin deleted a product | admin_id: %s",admin_access.id)

    return{"message":"Product deleted successfully!"}