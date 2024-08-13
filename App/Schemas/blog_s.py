from pydantic import BaseModel


class BlogDetail(BaseModel):
    title:str
    body:str
    status:str


class BlogUpdate(BaseModel):
    body: str
    status: str

