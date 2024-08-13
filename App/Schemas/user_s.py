from pydantic import BaseModel

class UserDetail(BaseModel):
    name:str
    email:str
    age:int
    activity_role:str
    password:str


class Login(BaseModel):
    username:str
    password:str


class UpdateUser(BaseModel):
    email: str
    age: int
    activity_role: str
