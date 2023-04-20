from pydantic import BaseModel
from typing import Optional


class PatternBase(BaseModel):
    text: str

    class Config:
        orm_mode = True


class PatternCreate(PatternBase):
    pass


class Pattern(PatternBase):
    id: int
    intent_id: int

    class Config:
        orm_mode = True


class ResponseBase(BaseModel):
    text: str

    class Config:
        orm_mode = True


class ResponseCreate(ResponseBase):
    pass


class Response(ResponseBase):
    id: int
    intent_id: int

    class Config:
        orm_mode = True


class IntentBase(BaseModel):
    tag: str
    patterns: list[PatternCreate]
    responses: list[ResponseCreate]


class IntentCreate(IntentBase):
    pass


class Intent(IntentBase):
    id: int

    class Config:
        orm_mode = True


class NPCBase(BaseModel):
    name: str
    avatar: Optional[str] = None
    bio: str
    voice: str
    style: str
    intents: list[Intent] = []


class NPCCreate(NPCBase):
    pass


class NPC(NPCBase):
    id: int

    class Config:
        orm_mode = True


class AvatarUpdate(BaseModel):
    avatar: str


class ProjectBase(BaseModel):
    name: str
    description: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    user_id: int
    npcs: list[NPC] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    projects: list[Project] = []

    class Config:
        orm_mode = True


class NPCIntentBase(BaseModel):
    pass


class NPCIntentCreate(NPCIntentBase):
    pass


class NPCIntent(NPCIntentBase):
    id: int
    npc_id: int
    intent_id: int

    class Config:
        orm_mode = True


class ProjectNPCBase(BaseModel):
    pass


class ProjectNPCCreate(ProjectNPCBase):
    pass


class ProjectNPC(ProjectNPCBase):
    id: int
    project_id: int
    npc_id: int

    class Config:
        orm_mode = True
