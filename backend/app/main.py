from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .db import Base, engine
from .routers import auth, products, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MotoShop API")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)

app.mount("/static", StaticFiles(directory="uploads"), name="static")
