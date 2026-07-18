from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from database import engine, Base, SessionLocal
import models
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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



class LabCreate(BaseModel):
    title: str
    deadline: str
    course_id: int


@app.post("/labs")
def create_lab(lab: LabCreate, db: Session = Depends(get_db)):
    new_lab = models.Lab(title=lab.title, deadline=lab.deadline, course_id=lab.course_id)
    db.add(new_lab)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="course_id does not exist")
    db.refresh(new_lab)
    return new_lab


@app.get("/labs")
def list_labs(db: Session = Depends(get_db)):
    return db.query(models.Lab).all()




class SubmissionCreate(BaseModel):
    lab_id: int
    student_name: str
    file_or_link: str


class SubmissionGrade(BaseModel):
    grade: int
    feedback: str


@app.post("/submissions")
def create_submission(sub: SubmissionCreate, db: Session = Depends(get_db)):
    new_sub = models.Submission(
        lab_id=sub.lab_id,
        student_name=sub.student_name,
        file_or_link=sub.file_or_link,
    )
    db.add(new_sub)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="lab_id does not exist")
    db.refresh(new_sub)
    return new_sub


@app.get("/submissions")
def list_submissions(db: Session = Depends(get_db)):
    return db.query(models.Submission).all()


@app.patch("/submissions/{submission_id}/grade")
def grade_submission(submission_id: int, grading: SubmissionGrade, db: Session = Depends(get_db)):
    sub = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    sub.grade = grading.grade
    sub.feedback = grading.feedback
    sub.status = "graded"
    db.commit()
    db.refresh(sub)
    return sub


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/app")
def serve_frontend():
    return FileResponse("static/index.html")


