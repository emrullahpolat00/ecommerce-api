from fastapi import FastAPI

from app.db import Base, engine
from app.models import tables  # noqa: F401  (modeller import edilsin diye)

from app.routers.users import router as users_router
from app.routers.categories import router as categories_router
from app.routers.products import router as products_router
from app.routers.orders import router as orders_router
from app.routers.reviews import router as reviews_router

app = FastAPI(
    title="E-Commerce REST API",
    version="1.0.0",
    description="Software Quality Assurance & Testing course project (FastAPI + SQLite).",
)


@app.on_event("startup")
def on_startup():
    # tabloları oluştur
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(users_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(reviews_router)