from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import customers, menu_items, orders, order_details, promotions, rating_reviews
from api.dependencies.database import engine
from api.models.model_loader import init_models
import uvicorn
import os

# Initialize FastAPI instance
app = FastAPI()

# CORS Middleware
origins = os.getenv("CORS_ORIGINS", "*").split(",")  # Use environment variable for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables during startup
@app.on_event("startup")
def startup_event():
    init_models(engine)  # Create tables if they don't exist


# Include Routers
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(menu_items.router, prefix="/menu-items", tags=["Menu Items"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(order_details.router, prefix="/order-details", tags=["Order Details"])
app.include_router(promotions.router, prefix="/promotions", tags=["Promotions"])
app.include_router(rating_reviews.router, prefix="/rating-reviews", tags=["Rating Reviews"])

# Root Endpoint
@app.get("/")
def health_check():
    return {"message": "API is running!"}


# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("APP_HOST", "127.0.0.1"), port=int(os.getenv("APP_PORT", 8000)))
