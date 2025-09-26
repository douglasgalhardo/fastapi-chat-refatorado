from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

from ..database import get_database
from ..models import MessageIn, MessageDB, MessageOut, MessageHistory

# Helper para serializar
def serialize_message(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    if isinstance(doc["created_at"], datetime):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc

router = APIRouter(tags=["REST Messages"])

@router.get("/rooms/{room}/messages", response_model=MessageHistory)
async def get_messages(
    room: str,
    limit: int = Query(20, ge=1, le=100),
    before_id: str | None = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    query: dict[str, Any] = {"room": room}
    if before_id:
        try:
            # Tratamento de erro explícito
            query["_id"] = {"$lt": ObjectId(before_id)}
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O ID '{before_id}' não é um ObjectId válido."
            )

    cursor = db["messages"].find(query).sort("_id", -1).limit(limit)
    docs = [MessageOut.parse_obj(d) async for d in cursor]
    docs.reverse()
    
    next_cursor = docs[0].id if docs else None
    return {"items": docs, "next_cursor": next_cursor}

@router.post("/rooms/{room}/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def post_message(
    room: str,
    message: MessageIn, # Uso de modelo Pydantic
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    
    message_db = MessageDB(room=room, **message.dict())
    
    res = await db["messages"].insert_one(message_db.dict(by_alias=True))
    
    # Dicionário para o MessageOut
    doc_out = message_db.dict()
    doc_out["_id"] = res.inserted_id
    
    return MessageOut.parse_obj(doc_out)