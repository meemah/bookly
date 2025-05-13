
from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from src.config import Config
import uuid
import logging

password_context = CryptContext(
    schemes=['bcrypt']
)
ACCESS_TOKEN_EXPIRY = 3600
def generate_passwd_hash(password:str)-> str:
    return password_context.hash(password)

def verify_password(secret:str, hashedPassword:str)-> bool:
    return password_context.verify(secret,hashedPassword)

def create_access_token(user_data: dict,expiry: timedelta = None, refresh:bool = False):
    payload = {}
    payload["user"]= user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY) )
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token = jwt.encode(
        payload=payload,
        key=Config.jwt_secret,
        algorithm=Config.jwt_algorithm
    )
    return token

def decode_access_token(token:str) -> dict:
    try:
        token_data = jwt.decode(jwt=token,key=Config.jwt_secret, algorithms=Config.jwt_algorithm)
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None