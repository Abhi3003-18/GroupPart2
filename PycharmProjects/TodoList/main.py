from multiprocessing.sharedctypes import synchronized

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

class TodoBase(BaseModel):
    id: int
    task_body: str
    due_day: int
    due_month: str
    due_year: int

@app.post("/todos/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoBase, db: db_dependency):
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    return {"detail": "Todo added successfully"}
@app.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(db: db_dependency):
    return db.query(models.Todo).all()

@app.put('/todos/{todo_id}', response_model=TodoBase, status_code=status.HTTP_200_OK)
async def update_todo(todo_id: int, todo_request: TodoBase, db: db_dependency):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id)
    if db_todo.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    update_data = todo_request.model_dump(exclude_unset=True)
    db_todo.update(update_data, synchronize_session=False)
    db.commit()
    return db_todo.first()


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: db_dependency):

    todo_to_delete = db.query(models.Todo).filter(models.Todo.id == todo_id).first()


    if not todo_to_delete:
        raise HTTPException(status_code=404, detail="Todo not found")


    db.delete(todo_to_delete)
    db.commit()
    return {"detail": "Todo deleted successfully"}