import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute, recipes, sandwiches, resources, reviews
from .models import model_loader
from .dependencies.config import conf


app = FastAPI()

# Allow all origins for CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
model_loader.index()

# Load routes dynamically (index)
indexRoute.load_routes(app)

# Explicitly include the recipes and sandwiches routers
app.include_router(recipes.router)
app.include_router(sandwiches.router)

app.include_router(resources.router)

app.include_router(reviews.router)


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)
