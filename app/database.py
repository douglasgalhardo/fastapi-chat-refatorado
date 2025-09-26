from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import MONGO_URL, MONGO_DB

class Database:
    
    client: Optional[AsyncIOMotorClient] = None

db_client = Database()

async def get_database() -> AsyncIOMotorDatabase:
    
    #Retorna uma instância do banco de dados para injeção de dependência.
  
    if db_client.client is None:
        raise Exception("Database client not initialized.")
    return db_client.client[MONGO_DB]

async def connect_to_mongo():
    #Conecta-se ao MongoDB
    if not MONGO_URL:
        raise RuntimeError("Defina MONGO_URL no .env (string do MongoDB Atlas).")
    print("Conectando ao MongoDB...")
    db_client.client = AsyncIOMotorClient(MONGO_URL)
    print("Conexão com MongoDB estabelecida.")

async def close_mongo_connection():
    #Fecha a conexão com o MongoDB no desligamento da aplicação
    print("Fechando conexão com MongoDB...")
    if db_client.client is not None:
        db_client.client.close()
    print("Conexão com MongoDB fechada.")