from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..database import get_database
from ..models import MessageDB, MessageOut
from ..ws_manager import manager

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws/{room}")
async def ws_room(
    websocket: WebSocket, 
    room: str, 
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    await manager.connect(room, websocket)
    try:
        # Envia o histórico inicial
        cursor = db["messages"].find({"room": room}).sort("_id", -1).limit(20)
        items = [MessageOut.parse_obj(d) async for d in cursor]
        items.reverse()
        await websocket.send_json({"type": "history", "items": [item.dict() for item in items]})

        while True:
            payload = await websocket.receive_json()
            username = str(payload.get("username", "anon"))[:50]
            content = str(payload.get("content", "")).strip()
            
            # ✅ TAREFA 3: Garante que mensagens sem conteúdo não sejam salvas
            if not content:
                continue

            message_db = MessageDB(room=room, username=username, content=content)
            res = await db["messages"].insert_one(message_db.dict(by_alias=True))

            doc_out = message_db.dict()
            doc_out["_id"] = res.inserted_id
            message_out = MessageOut.parse_obj(doc_out)
            
            await manager.broadcast(room, {"type": "message", "item": message_out.dict()})
            
    except WebSocketDisconnect:
        manager.disconnect(room, websocket)