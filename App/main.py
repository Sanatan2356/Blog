import uvicorn
from fastapi import FastAPI

from App.Database.db import engine,Base
from App.router import user_r,blog_r

app=FastAPI()
app.include_router(user_r.user_router)
app.include_router(blog_r.blog_router)
Base.metadata.create_all(bind=engine)


if __name__=='__main__':
    uvicorn.run(app,port=8500)
