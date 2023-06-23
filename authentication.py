from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
import jwt
from models import User
from fastapi import status


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def get_hashed_password(password):
    return pwd_context.hash(password)


async def verify_token(token: str):
    try: 
        payload = jwt.decode(token)
        user = await User.get(id = payload.get("id"))

    except:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED
        )
    
    return user