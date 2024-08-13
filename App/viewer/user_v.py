import traceback
from passlib.context import CryptContext
from App.Model.User_m import UserInfo
from App.Token.jwttoken import create_access_token, decode_token

pwd_cxt=CryptContext(schemes=['bcrypt'])

def hass_pwd(input_pass):
    try:
        hassing_pass=pwd_cxt.hash(input_pass)
        return hassing_pass
    except:
        print(traceback.print_exc())

def verify_password(plain_pass,hass_pass):
    try:
        vrf_pass=pwd_cxt.verify(plain_pass,hass_pass)
        return vrf_pass
    except:
        print(traceback.print_exc())




def user_add(request,db):
    try:
        if request.name is None:
            return 'Please insert your name.'
        elif request.email.split('@')[1] !='gmail.com':
            return 'please insert goggle email id'
        elif request.activity_role not in ['viewer','writer','admin']:
            return 'Please insert your activity role viewer and writer.'

        user_veri = db.query(UserInfo).filter(UserInfo.name == request.name).first()
        if  user_veri:
            return 'user already exist.'

        data=UserInfo(name=request.name,email=request.email,age=request.age,activity_role=request.activity_role,password=hass_pwd(request.password))
        db.add(data)
        db.commit()
        return 'User added successfully.'

    except:
        print(traceback.print_exc())


def login(request,db):
    try:

        user=db.query(UserInfo).filter(UserInfo.name==request.username).first()
        if not user:
            return 'User not found.'
        elif verify_password(request.password,user.password) ==False:
            return 'Invalid Password'
        access_token=create_access_token({'name':user.name,'email':user.email,'activity_role':user.activity_role})
        return {'token':access_token,'token_type':'barrer'}

    except:
        print(traceback.print_exc())


def viewuser(token):
    try:
        data=decode_token(token)
        if data['status'] != 200:
            return data['error']
        # print(data)
        return data['data']
    except:
        print(traceback.print_exc())


def delete_user(token,db):
    try:
        data = decode_token(token)
        if data['status'] != 200:
            return data['error']
        username = data['data']['name']
        user_veri=db.query(UserInfo).filter(UserInfo.name==username).first()
        if not user_veri:
            return 'user not found.'
        db.query(UserInfo).filter(UserInfo.name == username).delete(synchronize_session =False)
        db.commit()
        return 'user delete successfully.'


    except:
        print(traceback.print_exc())


def update_user(token,request,db):
    try:
        data=decode_token(token)
        if data['status'] != 200:
            return data['error']
        username=data['data']['name']
        user_veri=db.query(UserInfo).filter(UserInfo.name==username).first()
        if not user_veri:
            return 'user not found.'

        if request.email is None:
            request.email =user_veri.email
        elif request.activity_role is None:
            request.activity_role =user_veri.activity_role
        print(request.email)
        if request.email != '' or request.activity_role !='':
            if request.email.split('@')[1] != 'gmail.com':
                return 'please insert goggle email id'

            elif request.activity_role not in ['viewer', 'writer']:
                return 'Please insert your activity role viewer and writer.'


        update_data={'email':request.email,'age':request.age,'activity_role':request.activity_role}
        db.query(UserInfo).filter(UserInfo.name == username).update(update_data)
        db.commit()

        return 'data updated successfully.'

    except:
        print(traceback.print_exc())