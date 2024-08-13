from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

engine=create_engine('sqlite:///./Blog.db',connect_args={'check_same_thread':False})
local_session=sessionmaker(bind= engine,autoflush=False,autocommit=False)
Base=declarative_base()

db=local_session()

def get_db():
    try:
        yield db
    finally:
        db.close()