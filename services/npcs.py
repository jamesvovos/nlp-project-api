from sqlalchemy.orm import Session
from database import models
import schemas

# object-relational-mapping (ORM) crud operations (performs SQL under the hood)

# get NPC by ID


def get_npc(db: Session, npc_id: int):
    return db.query(models.NPC).filter(models.NPC.id == npc_id).first()

# get all NPCs


def get_npcs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.NPC).offset(skip).limit(limit).all()

# create a new NPC for a given project


def create_project_npc(db: Session, npc: schemas.NPCCreate, project_id: int):
    db_npc = models.NPC(**npc.dict(), project_id=project_id)
    db.add(db_npc)
    db.commit()
    db.refresh(db_npc)
    return db_npc

# delete NPC by ID


def delete_npc(db: Session, npc_id: int):
    db_npc = db.query(models.NPC).filter(
        models.NPC.id == npc_id).first()
    db.delete(db_npc)
    db.commit()
    return {"NPC Deleted": npc_id}

# update NPC by ID


def update_npc(db: Session, npc_id: int, npc: schemas.NPC):
    # get the NPC from the database
    db_npc = db.query(models.NPC).filter(
        models.NPC.id == npc_id).first()

    if db_npc:
        # update the name
        db_npc.name = npc.name
        # update the voice
        db_npc.voice = npc.voice
        # update the style
        db_npc.style = npc.style

        # constraint: can't update the project the NPC belongs to.

    db.commit()
    return db_npc
