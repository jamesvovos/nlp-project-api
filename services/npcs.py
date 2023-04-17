from sqlalchemy.orm import Session
from database import models
import schemas
from NpcTrainerAI.chat import ChatBot

# object-relational-mapping (ORM) crud operations (performs SQL under the hood)

# get NPC by ID


def get_npc(db: Session, npc_id: int):
    return db.query(models.NPC).filter(models.NPC.id == npc_id).first()

# get all NPCs


def get_npcs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.NPC).offset(skip).limit(limit).all()

# create a new NPC for a given project


def create_project_npc(db: Session, npc: schemas.NPCCreate, project_id: int):
    db_npc = models.NPC(**npc.dict())
    db_project = db.query(models.Project).filter(
        models.Project.id == project_id).first()
    db_project.npcs.append(db_npc)
    db.add(db_npc)
    db.commit()
    db.refresh(db_npc)
    db.refresh(db_project)
    return db_npc


# delete NPC by ID


def delete_npc(db: Session, npc_id: int):
    db_npc = db.query(models.NPC).filter(
        models.NPC.id == npc_id).first()
    project = db_npc.projects[0]
    project.npcs.remove(db_npc)
    db.delete(db_npc)
    db.commit()
    return {"NPC Deleted": npc_id}


# update NPC by ID / add intents to NPC


def update_npc(db: Session, npc_id: int, npc: schemas.NPC):
    # get the NPC from the database
    db_npc = db.query(models.NPC).filter(models.NPC.id == npc_id).first()

    if db_npc:
        # update the name
        db_npc.name = npc.name
        # update the avatar image
        db_npc.avatar = npc.avatar
        # update the bio
        db_npc.bio = npc.bio
        # update the voice
        db_npc.voice = npc.voice
        # update the style
        db_npc.style = npc.style

        # clear the existing intents
        db_npc.intents = []

        # add the selected intents
        for intent in npc.intents:
            intent = db.query(models.Intent).filter(
                models.Intent.id == intent.id).first()
            if intent:
                db_npc.intents.append(intent)

        db.commit()

    return db_npc

# get the intents associated with an npc via ID


def get_intents(db: Session, npc_id: int):
    # find the npc by ID
    db_npc = db.query(models.NPC).filter(
        models.NPC.id == npc_id).first()

    # create a list to store the intents
    intents = []

    # loop through each intent and extract its data
    for intent in db_npc.intents:
        intent_data = {
            'id': intent.id,
            'tag': intent.tag,
            'patterns': [p.text for p in intent.patterns],
            'responses': [r.text for r in intent.responses]
        }
        intents.append(intent_data)

    # return the list of intents
    return intents

# AI neural network response


def get_response(sentence: str, npc_id: int, training_required: bool):
    chatbot = ChatBot(training_required, npc_id)
    chatbot.setup()
    response = chatbot.get_response(sentence)
    response = {"AI says": response}
    return response
