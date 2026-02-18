from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    brand = Column(String(80), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    type = Column(String(20), nullable=False)  # "Motorcycle" або "Part"
    description = Column(String(1000), default="")
    image_url = Column(String(500), default="")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="New")
    total = Column(Numeric(10, 2), default=0)
    comment = Column(String(500), default="")

    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    title_snapshot = Column(String(120), nullable=False)
    price_snapshot = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1)

    order = relationship("Order", back_populates="items")
