from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship

from App.Database.db import Base


class BlogInfo(Base):
    __tablename__='Blog'
    id =Column(Integer,primary_key=True)
    title=Column(String)
    body=Column(String)
    status=Column(String)
    username=Column(String,ForeignKey('User.name'))
    created_at=Column(DateTime)
    updated_at=Column(DateTime)

    blog=relationship('UserInfo',backref='user')