import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path("../.env")
load_dotenv(dotenv_path=dotenv_path)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split()
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
JWT_SECRET=os.getenv("JWT_SECRET")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")