from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import session

from App.Database.db import get_db
from App.Schemas.blog_s import BlogDetail, BlogUpdate
from App.viewer.blog_v import blog_add, delete_blog, update_blog, view_blog, blog_upload, name_wise_blog_upload

blog_router=APIRouter(tags=['Blog'])



@blog_router.post('/addblog')
def add_blog(token:str,request:BlogDetail,db:session=Depends(get_db)):
    return blog_add(token,request,db)


@blog_router.get('/view_blog')
def add_blog(token:str,title:str,db:session=Depends(get_db)):
    return view_blog(token,title,db)


@blog_router.put('/update_blog')
def blog_update(token:str,title:str,request:BlogUpdate,db:session=Depends(get_db)):
    return update_blog(token,title,request,db)


@blog_router.delete('/delete_blog')
def blog_delete(token:str,title:str,db:session=Depends(get_db)):
    return delete_blog(token,title,db)


@blog_router.post('/upload_blogs')
def upload_blog(token:str,file:UploadFile=File(...),db:session=Depends(get_db)):
    return blog_upload(token,file,db)



@blog_router.post('/upload_blogs/username_wise')
def upload_blog_user(token:str,file:UploadFile=File(...),db:session=Depends(get_db)):
    return name_wise_blog_upload(token,file,db)