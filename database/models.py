from .database import Base
from sqlalchemy import Table, Integer, String, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship


# weak entity relationships:

ProjectNPC = Table('project_npcs', Base.metadata,
                   Column('project_id', Integer, ForeignKey('projects.id')),
                   Column('npc_id', Integer, ForeignKey('npcs.id'))
                   )

NPCIntent = Table('npc_intents', Base.metadata,
                  Column('npc_id', Integer, ForeignKey('npcs.id')),
                  Column('intent_id', Integer, ForeignKey('intents.id'))
                  )

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

    npcs = relationship("NPC", secondary="project_npcs",
                        back_populates="projects", lazy="joined")
    user = relationship("User", back_populates="projects")


class Intent(Base):
    __tablename__ = "intents"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, index=True)
    patterns = relationship("Pattern", back_populates="intent")
    responses = relationship("Response", back_populates="intent")
    npcs = relationship("NPC", secondary="npc_intents",
                        back_populates="intents")


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
    project_id = Column(Integer, ForeignKey("projects.id"))

    projects = relationship(
        "Project", secondary="project_npcs", back_populates="npcs")
    intents = relationship(
        "Intent", secondary="npc_intents", back_populates="npcs")
