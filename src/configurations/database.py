from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.utilities.models import Base
from src.configurations.initialize_env import DB_URL

engine = create_engine(DB_URL)

local_session = sessionmaker(autoflush=False,bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)