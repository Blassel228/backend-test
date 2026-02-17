from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.db.base import session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/login/")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_db():
    db = session()
    try:
        yield db
    finally:
        await db.close()
