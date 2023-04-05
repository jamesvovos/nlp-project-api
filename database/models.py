from .database import Base
from sqlalchemy import Integer, String, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship


# database ORM models and relationships


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    projects = relationship("Project", back_populates="user")


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="projects")


class Intent(Base):
    __tablename__ = "intents"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, index=True)
    patterns = relationship("Pattern", back_populates="intent")
    responses = relationship("Response", back_populates="intent")


class Pattern(Base):
    __tablename__ = "patterns"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"))

    intent = relationship("Intent", back_populates="patterns")


class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"))

    intent = relationship("Intent", back_populates="responses")


class NPC(Base):
    __tablename__ = "npcs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    voice = Column(String, index=True)
    style = Column(String, index=True)

    # intents = relationship("Intent", back_populates="npcs")

# weak entity relationships:


class NPCIntent(Base):
    __tablename__ = "npc_intents"
    id = Column(Integer, primary_key=True, index=True)
    npc_id = Column(Integer, ForeignKey("npcs.id"))
    intent_id = Column(Integer, ForeignKey("intents.id"))


class ProjectNPC(Base):
    __tablename__ = "project_npcs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    npc_id = Column(Integer, ForeignKey("npcs.id"))