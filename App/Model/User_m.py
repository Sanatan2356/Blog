from sqlalchemy import Column, Integer,String

from App.Database.db import  Base



class UserInfo(Base):
    __tablename__='User'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    email=Column(String)
    age=Column(Integer)
    activity_role=Column(String)
    password=Column(String)