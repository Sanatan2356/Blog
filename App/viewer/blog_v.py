import traceback
from datetime import datetime

import pandas as pd

from App.Model.User_m import UserInfo
from App.Model.blog_m import BlogInfo
from App.Token.jwttoken import decode_token


def blog_add(token,request,db):
    try:
        data = decode_token(token)
        if data['status'] != 200:
            return data['error']
        username = data['data']['name']

        if request.title =='':
            return 'please insert your blog title'

        if request.body =='':
            return 'please insert your blog body.'

        elif len(request.body) <50:
            return 'in blog add minimaze 100 character.'

        elif request.status not  in ['public','private']:
            return 'in blog  2 type of status public and private.'

        user_veri = db.query(UserInfo).filter(UserInfo.name == username).first()
        if not user_veri:
            return 'user not found.'
        elif user_veri.activity_role =='viewer':
            return 'you are not add blog.'

        blog_add=BlogInfo(title=request.title,body=request.body,status=request.status,username=username,created_at=datetime.utcnow())

        db.add(blog_add)
        db.commit()
        return 'blog is created successfully.'


    except:
        print(traceback.print_exc())

def view_blog(token,title,db):
    try:
        data = decode_token(token)
        if data['status'] != 200:
            return data['error']
        username = data['data']['name']
        user_veri = db.query(UserInfo).filter(UserInfo.name == username).first()
        if not user_veri:
            return 'user not found.'

        elif user_veri.activity_role !='viewer':
            return 'blogs view only that activity role is  viewer.'

        if title == '':
            all_blogs=db.query(BlogInfo).all()
            list=[]
            for row in all_blogs:
                dict_blog={'title':row.title,
                           'body':row.body,
                           'created_at':row.created_at}
                list.append(dict_blog)
            return list

        blogs=db.query(BlogInfo).filter(BlogInfo.title ==title).first()

        if blogs.status !='public':
            return 'this blog is private mode.'


        return {'title':blogs.title,'body':blogs.body,'created_at':blogs.created_at}



    except:
        print(traceback.print_exc())


def update_blog(token,title,request,db):
    try:
        data = decode_token(token)
        if data['status'] != 200:
            return data['error']
        username = data['data']['name']
        blogs=db.query(BlogInfo).filter(BlogInfo.title ==title).first()
        if blogs.username != username:
            return 'Invalid User'
        if request.body == '':
            request.body=blogs.body
        elif request.status == '':
            request.status=blogs.status

        update_blog={'body':request.body,'status':request.status,'updated_at':datetime.utcnow()}
        db.query(BlogInfo).filter(BlogInfo.title ==title).update(update_blog)
        db.commit()
        return 'blog update successfully.'

    except:
        print(traceback.print_exc())



def delete_blog(token,title,db):
    try:
        data = decode_token(token)
        if data['status'] != 200:
            return data['error']
        username = data['data']['name']

        db.query(BlogInfo).filter(BlogInfo.title ==title and BlogInfo.username ==username).delete(synchronize_session =False)
        db.commit()
        return 'blog is deleted successfully.'

    except:
        print(traceback.print_exc())


def blog_upload(token,file,db):
    try:

        data = decode_token(token)
        if data['status'] != 200:
            return data['error']
        username = data['data']['name']
        user_veri = db.query(UserInfo).filter(UserInfo.name == username).first()
        if not user_veri:
            return 'user not found.'
        elif user_veri.activity_role == 'viewer':
            return 'you are not add blog.'

        df=pd.read_csv(file.filename)
        blog_title=db.query(BlogInfo).all()
        list1=[]
        for blog in blog_title:
            blog_t=blog.title
            list1.append(blog_t)

        for index,row  in df.iterrows():
            if row['title'] in list1:
                continue

            data=BlogInfo(title=row['title'],body=row['body'],status=row['status'],username=username,created_at=datetime.utcnow())
            db.add(data)
            db.commit()
        return f'{file.filename} uploaded successfully'

    except:
        print(traceback.print_exc())



def name_wise_blog_upload(token,file,db):
    try:

        data = decode_token(token)
        if data['status'] != 200:
            return data['error']

        if data['data']['activity_role'] !='admin':
            return 'this file upload by admin'




        df=pd.read_csv(file.filename)

        blog_title=db.query(BlogInfo).all()
        list1=[]
        for blog in blog_title:
            blog_t=blog.title
            list1.append(blog_t)



        for index,row  in df.iterrows():
            if row['title'] in list1:
                continue
            user_veri = db.query(UserInfo).filter(UserInfo.name == row['username']).first()
            if not user_veri:
                continue
            elif user_veri.activity_role == 'viewer':
                continue

            data=BlogInfo(title=row['title'],body=row['body'],status=row['status'],username=row['username'],created_at=datetime.utcnow())
            db.add(data)
            db.commit()
        return f'{file.filename} uploaded successfully'

    except:
        print(traceback.print_exc())