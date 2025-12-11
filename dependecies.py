from database import local_session

def get_session():
    session = local_session()
    try:
        yield session
    finally:
        session.close()