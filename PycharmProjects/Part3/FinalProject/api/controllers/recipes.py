from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import recipes as model
from ..models import sandwiches as sandwich_model
from ..models import resources as resource_model
from ..schemas.recipes import RecipeCreate, RecipeUpdate


def create(db: Session, request: RecipeCreate):
    # Validate foreign keys
    sandwich = db.query(sandwich_model.Sandwich).filter(sandwich_model.Sandwich.id == request.sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    resource = db.query(resource_model.Resource).filter(resource_model.Resource.id == request.resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    # Create a new Recipe
    new_recipe = model.Recipe(
        sandwich_id=request.sandwich_id,
        resource_id=request.resource_id,
        amount=request.amount,
    )
    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_recipe


def read_all(db: Session):
    try:
        result = db.query(model.Recipe).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, recipe_id: int):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return recipe


def update(db: Session, recipe_id: int, request: RecipeUpdate):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        if not recipe.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

        # Validate foreign keys if updating sandwich_id or resource_id
        if request.sandwich_id:
            sandwich = db.query(sandwich_model.Sandwich).filter(sandwich_model.Sandwich.id == request.sandwich_id).first()
            if not sandwich:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
        if request.resource_id:
            resource = db.query(resource_model.Resource).filter(resource_model.Resource.id == request.resource_id).first()
            if not resource:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

        # Perform the update
        update_data = request.dict(exclude_unset=True)
        recipe.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return recipe.first()


def delete(db: Session, recipe_id: int):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        if not recipe.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        recipe.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
