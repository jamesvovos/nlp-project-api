from sqlalchemy.orm import Session
from database import models
import schemas

# object-relational-mapping (ORM) crud operations (performs SQL under the hood)

# get project by ID


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

# get all projects


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

# create a new project for a given user


def create_user_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(**project.dict(), user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# delete project by ID


def delete_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(
        models.Project.id == project_id).first()
    db.delete(db_project)
    db.commit()
    return {"Project Deleted": project_id}

# update project by ID


def update_project(db: Session, project_id: int, project: schemas.Project):
    # get the project from the database
    db_project = db.query(models.Project).filter(
        models.Project.id == project_id).first()

    if db_project:
        # update the name
        db_project.name = project.name
        # update the description
        db_project.description = project.description

    db.commit()
    return db_project
