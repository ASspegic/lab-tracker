"""
Automated tests for the Course Lab Submission Tracker API.

Run with:  pytest
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base

# --- Use a separate database just for tests, so real data is never touched ---
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Tell FastAPI: whenever a route asks for get_db, use our test version instead
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_course():
    response = client.post("/courses", json={"name": "Databases", "code": "DB101"})
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "DB101"
    assert "id" in data


def test_list_courses():
    response = client.get("/courses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_lab_with_valid_course():
    course = client.post("/courses", json={"name": "Web Dev", "code": "WD101"}).json()
    response = client.post("/labs", json={
        "title": "Lab 1: Setup",
        "deadline": "2026-08-01",
        "course_id": course["id"],
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Lab 1: Setup"


def test_create_lab_with_invalid_course_is_rejected():
    response = client.post("/labs", json={
        "title": "Ghost Lab",
        "deadline": "2026-08-01",
        "course_id": 999999,
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "course_id does not exist"


def test_create_submission_and_grade_it():
    course = client.post("/courses", json={"name": "AI", "code": "AI101"}).json()
    lab = client.post("/labs", json={
        "title": "Lab X",
        "deadline": "2026-08-05",
        "course_id": course["id"],
    }).json()

    submission = client.post("/submissions", json={
        "lab_id": lab["id"],
        "student_name": "Alice",
        "file_or_link": "https://github.com/alice/lab-x",
    }).json()
    assert submission["status"] == "submitted"
    assert submission["grade"] is None

    graded = client.patch(f"/submissions/{submission['id']}/grade", json={
        "grade": 90,
        "feedback": "Good job",
    })
    assert graded.status_code == 200
    graded_data = graded.json()
    assert graded_data["grade"] == 90
    assert graded_data["status"] == "graded"


def test_grading_nonexistent_submission_returns_404():
    response = client.patch("/submissions/999999/grade", json={
        "grade": 100,
        "feedback": "N/A",
    })
    assert response.status_code == 404
