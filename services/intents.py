from sqlalchemy.orm import Session
from database import models
import schemas

# object-relational-mapping (ORM) crud operations (performs SQL under the hood)


# read
def get_intents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Intent).offset(skip).limit(limit).all()


# create
def create_intent(db: Session, intent: schemas.IntentCreate):
    db_intent = models.Intent(
        tag=intent.tag
    )
    db.add(db_intent)
    db.commit()
    db.refresh(db_intent)

    # Create and add patterns to the intent
    for pattern in intent.patterns:
        print(f'pattern text: {pattern.text}')
        db_pattern = models.Pattern(
            text=pattern.text,
            intent_id=db_intent.id
        )
        db.add(db_pattern)

    # Create and add responses to the intent
    for response in intent.responses:
        print(f'response text: {response.text}')
        db_response = models.Response(
            text=response.text,
            intent_id=db_intent.id
        )
        db.add(db_response)

    db.commit()
    db.refresh(db_intent)
    return db_intent


# create a pattern{} for intent


def create_intent_pattern(db: Session, pattern: schemas.PatternCreate, intent_id: int):
    db_pattern = models.Pattern(text=pattern.text, intent_id=intent_id)
    db.add(db_pattern)
    db.commit()
    db.refresh(db_pattern)
    return db_pattern

# create a response{} for intent


def create_intent_response(db: Session, response: schemas.ResponseCreate, intent_id: int):
    db_pattern = models.Response(text=response.text, intent_id=intent_id)
    db.add(db_pattern)
    db.commit()
    db.refresh(db_pattern)
    return db_pattern
