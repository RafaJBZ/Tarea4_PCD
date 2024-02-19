from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    user_name: str = Field(min_length=1)
    user_email: str = Field(min_length=1)
    age: int
    recommendations: str = Field(min_length=1)
    ZIP: int


USERS = []

@app.get("/")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@app.post("/")
def create_user(user: User, db: Session = Depends(get_db)):

    # Verificar si ya existe un usuario con el mismo correo electrónico
    existing_user = db.query(models.Users).filter(models.Users.user_email == user.user_email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    user_model = models.Users()
    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.ZIP = user.ZIP

    db.add(user_model)
    db.commit()

    return user


@app.put("/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} does not exist"
        )

    if user.user_email != user_model.user_email:
        existing_user = db.query(models.Users).filter(models.Users.user_email == user.user_email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Another user with this email already exists"
            )

    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.ZIP = user.ZIP

    db.commit()

    return user

@app.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} : Does not exist"
        )

    return user_model


@app.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} : Does not exist"
        )

    db.query(models.Users).filter(models.Users.user_id == user_id).delete()

    db.commit()

if __name__ == "__main__":
    config  = uvicorn.Config("main:app", port=5050, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()