from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.dependecies import get_session,pagination_params,get_current_user
from app.database import models
from app import schemas
from app.operations import operations

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

#===============================
    #GET ALL ITEMS FROM CART
#===============================
@router.get("/cart/products",response_model= schemas.Paginated_Response[schemas.Product_Out])
def get_all_items_from_cart(pagination = Depends(pagination_params),
                            current_user = Depends(get_current_user),
                            session: Session = Depends(get_session)):

    db_cart_products = session.query(models.Cart_Product).filter(models.Cart_Product.cart_id==current_user.id).all()
    db_products = []
    for db_cart_product in db_cart_products:
        db_product = session.query(models.Product).filter(models.Product.id==db_cart_product.product_id).first()
        db_products.append(db_product)

    total = db_products.count()
    if not total:
        raise HTTPException(status_code=404,detail="There is no items in the cart yet!")

    return {"total":total,"page":pagination["page"],"limit":pagination["limit"],"items": db_products}

#===============================
        #ADD ITEM TO CART
#===============================
@router.post("/cart/products/{product_id}",response_model=schemas.Base_Cart_Out)
def add_item_to_cart(product_id: int, quantity: int,
                     current_user = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    
    try:
        item = operations.get_product_by_id(product_id)
        
        #CHECKS IF STOCK IS STILL SUFFICIENT
        if quantity > item.stock:
            raise HTTPException(status_code=400,detail="Insufficient product stock!")

        cart_product_link = (session.query(models.Cart_Product)
                .filter(models.Cart_Product.cart_id==current_user.id,
                        models.Cart_Product.product_id==item.id)
                .first())
        #IF EXIST, THE QUANTITY WILL BE JUST ADDED
        if cart_product_link:
            cart_product_link.quantity += quantity

        #IF NOT, CREATE NEW CART_PRODUCT
        if not cart_product_link:
            new_link = models.Cart_Product(
                cart_id = current_user.id,
                product_id = item.id,
                quantity = quantity
            )
            session.add(new_link)

        session.commit()
        session.refresh(current_user.cart)

        logger.info("User added an item to the cart | user_id: %s",current_user.id)

        return current_user.cart
    
    except HTTPException:
        session.rollback()
        raise

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500,detail="Checkout failed") from e

#===============================
    #REMOVE ITEM FROM CART
#===============================
@router.put("/cart/products/{product_id}")
def remove_item_from_cart(product_id: int,
                        current_user = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    
    try:
        item = operations.get_product_by_id(product_id)
        
        #CHECKS IF THE ITEM IS IN THE CART
        db_cart_product = (session.query(models.Cart_Product)
                .filter(models.Cart_Product.cart_id==current_user.id,
                        models.Cart_Product.product_id==item.id)
                .first())
        if not db_cart_product:
            raise HTTPException(status_code=404,detail="Item is not in the cart!")
        
        session.delete(db_cart_product)
        session.commit()
        session.refresh(current_user.cart)

        logger.info("User removed  an item to the cart | user_id: %s",current_user.id)

        return {"message":f"{item.name} is removed from the cart successfully!"}
    
    except HTTPException:
        session.rollback()
        raise

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500,detail="Checkout failed") from e

#===============================
    #CHECKOUT ITEMS FROM CART
#===============================
@router.put("/cart")
def checkout(product_id_list: list[int],
            order: schemas.Order_Create,
            current_user = Depends(get_current_user),
            session: Session = Depends(get_session)):
    
    try:
        #GET ALL THE ITEMS FROM THE CURRENT USER'S CART
        cart_products = session.query(models.Cart_Product).filter(models.Cart_Product.cart_id==current_user.id).all()
        if not cart_products:
            raise HTTPException(status_code=404,detail="There is no item in the cart!")

        #MATCH THE SELECTED ITEMS FROM THE ITEMS IN THE CART
        for product_id in product_id_list:
            for cart_product in cart_products:
                if product_id == cart_product.product_id:

                    order_input: schemas.Base_Order_Create
                    order_input.payment_method = order.payment_method
                    order_input.payment_status = order.payment_status
                    order_input.product_id = product_id
                    order_input.product_quantity = cart_product.quantity

                    operations.add_new_order(current_user.id,order_input)

                    cart_product_link = session.query(models.Cart_Product).filter(models.Cart_Product.cart_id==current_user.id,
                                                                models.Cart_Product.product_id==product_id).first()
                    session.delete(cart_product_link)
                    session.flush()

        session.commit()
        return {"message":"Checkout successful!"}
    
    except HTTPException:
        session.rollback()
        raise

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500,detail="Checkout failed") from e

#===============================
    #CHECKOUT ALL ITEMS FROM CART
#===============================
@router.post("/cart")
def checkout_all_items( order: schemas.Order_Create,
                       current_user = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    
    try:
        #GET ALL THE ITEMS FROM THE CURRENT USER'S CART
        cart_products = session.query(models.Cart_Product).filter(models.Cart_Product.cart_id==current_user.id).all()
        if not cart_products:
            raise HTTPException(status_code=404,detail="There is no item in the cart!")

        #ITERATE THROUGH ALL THE ITEMS IN THE CART
        for cart_product in cart_products:

            order_input: schemas.Base_Order_Create
            order_input.payment_method = order.payment_method
            order_input.payment_status = order.payment_status
            order_input.product_id = cart_product.product_id
            order_input.product_quantity = cart_product.quantity

            operations.add_new_order(current_user.id,order_input)

        session.commit()
        return {"message":"Checkout successful!"}
    
    except HTTPException:
        session.rollback()
        raise

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500,detail="Checkout failed") from e