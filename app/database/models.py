from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String,Integer,Column,ForeignKey,Float,UniqueConstraint,DateTime,JSON,Boolean
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime,timezone

from app.database import engine

Base = declarative_base()

class User():
    __tablename__ = "Users"

    id = Column(String(4),default=lambda: uuid4().hex[:4] ,primary_key=True,nullable=False,unique=True)
    role = Column(String,default="user")
    username = Column(String)
    email = Column(String)
    password = Column(String)

    fullname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    occupation = Column(String)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    cart = relationship("Cart",back_populates="user",uselist=False,cascade="all, delete-orphan")

class Cart():
    __tablename__ = "Carts"

    user_id = Column(String(4),ForeignKey("Users.id",ondelete="CASCADE"),primary_key=True,unique=True,nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User",back_populates="user",uselist=False)
    orders = relationship("Order",back_populates="cart")

class Order():
    __tablename__ = "Orders"

    id = Column(String(8),default=lambda: uuid4().hex[:8] ,primary_key=True,nullable=False,unique=True)
    cart_id = Column(String(4),ForeignKey("Carts.user_id",ondelete="CASCADE"),unique=False,nullable=False)
    status = Column(String,default="pending")
    checked_out = Column(Boolean,default=False)
    payment_method = Column(String,default=None)
    payment_status = Column(String,default=None)

    ordered_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    cart = relationship("Cart",back_populates="orders")
    order_products = relationship("Order_Product",back_populates="order")
    products = relationship("Product")

class Order_Product():
    __tablename__ = "Order_Products"
    __table_args__ = (UniqueConstraint("order_id","product_id",name="uq_order_product"),)

    order_id = Column(String(8),ForeignKey("Orders.id",ondelete="CASCADE"),unique=False,nullable=False)
    product_id = Column(String(4),ForeignKey("Products.id",ondelete="CASCADE"),unique=False,nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    order = relationship("Order",back_populates="order_products")
    product = relationship("Product",back_populates="product_orders")

class Product():
    __tablename__ = "Products"

    id = Column(String(4),default=lambda: uuid4().hex[:4] ,primary_key=True,nullable=False,unique=True)
    name = Column(String)
    details = Column(JSON,default={"category":None,"color":None,"desctiption":None})
    price = Column(Float)
    stock = Column(Integer)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    product_orders = relationship("Order_Product",back_populates="product")
    orders = relationship("Order")

Base.metadata.create_all(bind=engine)