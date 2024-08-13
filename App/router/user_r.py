from fastapi import APIRouter, Depends
from sqlalchemy.orm import session

from App.Database.db import get_db
from App.Schemas.user_s import UserDetail, Login, UpdateUser
from App.viewer.user_v import user_add, login, delete_user, update_user, viewuser

user_router=APIRouter(tags=['User'])


@user_router.post('/add_user')
def add_user(request:UserDetail,db:session=Depends(get_db)):
    return user_add(request,db)


@user_router.post('/login')
def sign_in(request:Login,db:session=Depends(get_db)):
    return login(request,db)



@user_router.post('/login')
def sign_in(request:Login,db:session=Depends(get_db)):
    return login(request,db)


@user_router.get('/view_user')
def view_user(token:str):
    return viewuser(token)


@user_router.put('/update_user')
def user_update(token:str,request:UpdateUser,db:session=Depends(get_db)):
    return update_user(token,request,db)



@user_router.delete('/delete_user')
def user_delete(token:str,db:session=Depends(get_db)):
    return delete_user(token,db)