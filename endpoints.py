from fastapi import FastAPI, HTTPException, Depends
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
import schemas
from services import users, projects, intents
from database import models


models.Base.metadata.create_all(bind=engine)

# Inject database dependencies into FastAPI
# Independent database session/connection per requestm, closes the session after request is finished.


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create FastAPI object
app = FastAPI()


# API Requests/Endpoints

# root api endpoint
@app.get("/")
def get_root(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_intents = intents.get_intents(db, skip=skip, limit=limit)
    return db_intents

# create user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users.create_user(db=db, user=user)

# get all users


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = users.get_users(db, skip=skip, limit=limit)
    return db_users

# get user by ID


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# # NOTE: NEW** create project for a user


@app.post("/users/{user_id}/projects/", response_model=schemas.Project)
def create_project_for_user(
    user_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    return projects.create_user_project(db=db, project=project, user_id=user_id)

# get all projects


@app.get("/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_projects = projects.get_projects(db, skip=skip, limit=limit)
    return db_projects

# get all intents


@app.get("/intents/", response_model=list[schemas.Intent])
def read_intents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_intents = intents.get_intents(db, skip=skip, limit=limit)
    return db_intents

# create intent


@app.post("/intents/create/", response_model=schemas.Intent)
def create_intent(intent: schemas.IntentCreate, db: Session = Depends(get_db)):
    existing_intent = db.query(models.Intent).filter_by(
        tag=intent.tag).first()
    if existing_intent:
        raise HTTPException(
            status_code=400, detail="Intent with that tag already exists")
    return intents.create_intent(db=db, intent=intent)


# create pattern for intent


@app.post("/intents/{intent_id}/patterns/", response_model=schemas.Pattern)
def create_intent_pattern(
    intent_id: int, pattern: schemas.PatternCreate, db: Session = Depends(get_db)
):
    # Get the intent from the database
    db_intent = db.query(models.Intent).filter(
        models.Intent.id == intent_id).first()

    # If the intent does not exist, raise an HTTPException with a 404 status code
    if not db_intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    return intents.create_intent_pattern(db=db, pattern=pattern, intent_id=intent_id)

# create response for intent


@app.post("/intents/{intent_id}/responses/", response_model=schemas.Response)
def create_intent_response(
    intent_id: int, response: schemas.ResponseCreate, db: Session = Depends(get_db)
):
    # Get the intent from the database
    db_intent = db.query(models.Intent).filter(
        models.Intent.id == intent_id).first()

    # If the intent does not exist, raise an HTTPException with a 404 status code
    if not db_intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    return intents.create_intent_response(db=db, response=response, intent_id=intent_id)