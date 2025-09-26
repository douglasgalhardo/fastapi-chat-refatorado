from typing import Dict, Set
from fastapi import WebSocket

class WSManager:
    """Gerencia as salas de chat e as conexões WebSocket."""
    def __init__(self):
        """Inicializa o gerenciador com um dicionário vazio de salas."""
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        """Aceita uma nova conexão e a adiciona a uma sala."""
        await ws.accept()
        self.rooms.setdefault(room, set()).add(ws)

    def disconnect(self, room: str, ws: WebSocket):
        """Desconecta um WebSocket e remove da sala, limpando a sala se estiver vazia."""
        conns = self.rooms.get(room)
        if conns and ws in conns:
            conns.remove(ws)
            if not conns:
                self.rooms.pop(room, None)

    async def broadcast(self, room: str, payload: dict):
        """Envia uma mensagem JSON para todos os clientes em uma sala."""
        # Usamos list() para criar uma cópia, pois a desconexão pode alterar o set durante a iteração
        for ws in list(self.rooms.get(room, [])):
            try:
                await ws.send_json(payload)
            except Exception:
                # Se o envio falhar, o cliente provavelmente desconectou.
                self.disconnect(room, ws)

# Instância global (Singleton) para ser usada pela aplicação
manager = WSManager()