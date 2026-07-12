from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, unique=True)

class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Integer)
    deadline = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.id"))
    student_name = Column(String)
    file_or_link = Column(String)
    status = Column(String, default="submitted")
    grade = Column(Integer, nullable=True)
    feedback = Column(String, nullable=True)