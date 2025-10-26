from sqlalchemy.orm import create_session ,sessionmaker
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from utils.imports import * 
Base = declarative_base()

engine = create_engine(DB_URL)

session = sessionmaker(bind=engine,autoflush=False)


def ConnectDB():
    db = session()
    try :
        print('Connection established !')
        yield db
    except Exception:
        db.close_all()
        print('Connection closed !')