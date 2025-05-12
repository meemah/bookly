import redis.asyncio as redis
from src.config import Config
JTI_EXPIRY=3600
token_blocklist =redis.Redis(
    host=Config.redis_host,
    port=Config.redis_port,
    db=0
)

async def add_jti_to_blocklist(jti:str)->None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )

async def jti_in_blocklist(jti:str)-> bool:
    return True if  await token_blocklist.get(jti) is not None else False 