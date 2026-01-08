from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.database.models import Base
from src.core.config import ENV

import os

DB_URL = os.getenv('DB_URL')
if not DB_URL:
    raise RuntimeError("DB_URL is not set")

engine = create_engine(DB_URL)

local_session = sessionmaker(autoflush=False,bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)