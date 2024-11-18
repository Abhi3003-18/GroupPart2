from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status, Response
from ..models import models, schemas


def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    new_recipe = models.Recipe(
        amount=recipe.amount,
        sandwich_id=recipe.sandwich_id,
        resource_id=recipe.resource_id
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


def update_recipe(db: Session, recipe_id: int, recipe: schemas.RecipeUpdate):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    for var, value in vars(recipe).items():
        setattr(db_recipe, var, value) if value is not None else None
    db.commit()
    return db_recipe


def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def read_all_recipes(db: Session):
    return db.query(models.Recipe).options(joinedload(models.Recipe.sandwich), joinedload(models.Recipe.resource)).all()


def read_one_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).options(joinedload(models.Recipe.sandwich), joinedload(models.Recipe.resource)).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe