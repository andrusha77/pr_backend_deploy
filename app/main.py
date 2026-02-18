from fastapi import FastAPI
from .db import Base, engine
from .routers import auth, products, orders
from .routers import images

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MotoShop API")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(images.router)
from fastapi import FastAPI

app = FastAPI(title="MotoShop API")

@app.get("/")
def root():
    return {"ok": True, "message": "MotoShop API is running"}
