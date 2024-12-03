from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader, customers, menu_items, order_details, orders, payments, promotions, rating_reviews, recipes, resources, sandwiches
from .dependencies.config import conf
from .dependencies.database import engine, get_db
from .controllers import orders, order_details
from sqlalchemy.orm import Session






model_loader.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)