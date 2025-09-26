from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

class MessageBase(BaseModel):
    """Modelo base para mensagens."""
    username: str = Field(..., max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)

class MessageIn(MessageBase):
    """Modelo para a entrada de dados ao criar uma nova mensagem via REST."""
    pass

class MessageDB(MessageBase):
    """Modelo que representa uma mensagem como ela é armazenada no DB."""
    room: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MessageOut(BaseModel):
    """Modelo para a saída de dados, formatando os campos do DB."""
    id: str = Field(..., alias="_id")
    room: str
    username: str
    content: str
    created_at: str

    @field_validator('id', mode='before')
    @classmethod
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @field_validator('created_at', mode='before')
    @classmethod
    def format_datetime(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class MessageHistory(BaseModel):
    """Modelo para a resposta da rota de histórico de mensagens."""
    items: List[MessageOut]
    next_cursor: Optional[str] = None