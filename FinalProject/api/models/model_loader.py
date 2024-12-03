from sqlalchemy.orm import Session
from ..models.customers import Customer
from ..models.menu_items import MenuItem
from ..models.order_details import OrderDetail
from ..models.orders import Order
from ..models.payments import Payment
from ..models.promotions import Promotion
from ..models.rating_reviews import RatingReview
from ..models.recipes import Recipe
from ..models.resources import Resource
from ..models.sandwiches import Sandwich
from ..dependencies.database import Base, engine


def init_models(engine=engine):
    """
    Initialize all models by creating the database tables.
    Call this function during app startup.
    """
    print("Initializing database models...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
