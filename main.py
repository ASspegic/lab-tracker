from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import engine, Base, SessionLocal
import models

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CourseCreate(BaseModel):
    name: str
    code: str

@app.get("/courses")
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


@app.get("/")
def home():
    return {"message": "Hello, lab tracker!"}


@app.post("/courses")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(name=course.name, code=course.code)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course