from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
import schemas
from services import users, projects, intents, npcs
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

# Set up CORS middleware
origins = ["http://localhost",    "http://localhost:3000", ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

# delete intent by ID


@app.delete("/intents/{intent_id}/")
def delete_intent(intent_id: int, db: Session = Depends(get_db)):
    db_intent = intents.get_intent(db, intent_id=intent_id)
    if db_intent is None:
        raise HTTPException(
            status_code=404, detail="Intent with that ID not found")
    return intents.delete_intent(db=db, intent_id=intent_id)

# update intent by ID


@app.put("/intents/{intent_id}/", response_model=schemas.Intent)
def update_intent(intent_id: int, intent: schemas.IntentCreate, db: Session = Depends(get_db)):
    db_intent = intents.get_intent(db, intent_id=intent_id)
    if db_intent is None:
        raise HTTPException(
            status_code=404, detail="Intent with that ID not found")
    return intents.update_intent(db=db, intent_id=intent_id, intent=intent)


# delete project by ID


@app.delete("/projects/{project_id}/")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = projects.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(
            status_code=404, detail="Project with that ID not found")
    return projects.delete_project(db=db, project_id=project_id)


# update project by ID


@app.put("/projects/{project_id}/", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = projects.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(
            status_code=404, detail="Project with that ID not found")
    return projects.update_project(db=db, project_id=project_id, project=project)


# # # NOTE: NEW** create NPC for project


@app.post("/projects/{project_id}/npc/", response_model=schemas.NPC)
def create_npc_for_project(
    project_id: int, npc: schemas.NPCCreate, db: Session = Depends(get_db)
):
    return npcs.create_project_npc(db=db, npc=npc, project_id=project_id)

# get all NPCs


@app.get("/npcs/", response_model=list[schemas.NPC])
def read_npcs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_npcs = npcs.get_npcs(db, skip=skip, limit=limit)
    return db_npcs


# delete NPC by ID


@app.delete("/npcs/{npc_id}/")
def delete_npc(npc_id: int, db: Session = Depends(get_db)):
    db_npc = npcs.get_npc(db, npc_id=npc_id)
    if db_npc is None:
        raise HTTPException(
            status_code=404, detail="NPC with that ID not found")
    return npcs.delete_npc(db=db, npc_id=npc_id)


# update NPC by ID


@app.put("/npcs/{npc_id}/", response_model=schemas.NPC)
def update_npc(npc_id: int, npc: schemas.NPCCreate, db: Session = Depends(get_db)):
    db_npc = npcs.get_npc(db, npc_id=npc_id)
    if db_npc is None:
        raise HTTPException(
            status_code=404, detail="NPC with that ID not found")
    return npcs.update_npc(db=db, npc_id=npc_id, npc=npc)
