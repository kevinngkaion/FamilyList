# This file is responsible for signing, encoding, decoding, and returning JWTs
import time
from jose import jwt, JWTError
from config import JWT_ALGORITHM, JWT_SECRET
from datetime import timedelta, datetime
# This function signs the JWT string
def create_access_token(username:str, uid: str, expires_delta: timedelta or None = None):
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=10)
    payload = {
        "sub": username,
        "id": str(uid),
        "exp": expires
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decodeJWT(token:str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['exp'] >= time.time() else None
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")