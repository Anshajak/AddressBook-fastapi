from typing import Union, List
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import uvicorn
import models
from pydantic import BaseModel
import schemas
import operations as crud

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates=Jinja2Templates(directory="templates")

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

@app.get('/', response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("home.html",{'request':request})

@app.get('/admin/user')
def showUserAdmin(request:Request, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        if not crud.checkAdmin(token, db):
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")

    user_id = request.query_params.get('user_id', None)
    email = request.query_params.get('email', None)
    user=[]
    if user_id!= None and email!=None:
        user.append(crud.get_user_by_email(db,email))
        user.append(crud.get_user(db,int(user_id)))
    elif user_id== None and email!=None:
        user=crud.get_user_by_email(db,email)
    elif user_id!= None and email==None:
        user=crud.get_user(db,int(user_id))
    else:
        user=crud.get_users(db)
    return {"user":user,"user_id":user_id,"email":email}

@app.get('/admin/user/add')
def addUserAdmin(request:Request, user_request:schemas.AdminCreate, db: Session = Depends(get_db)):
    user=crud.create_admin(db,user_request)
    return user

@app.get('/admin/user/edit')
def editUserAdmin(request:Request, user_request:schemas.AdminCreate, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        if not crud.checkAdmin(token, db):
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    user_id = request.query_params.get('user_id', None)
    username = request.query_params.get('username', None)
    email = request.query_params.get('email', None)
    user=[]
    if user_id!=None:
        user.append(crud.edit_user_by_Id(db, user_request, user_id))
    if username!=None:
        user.append(crud.edit_user_by_username(db, user_request, username))
    if email!=None:
        user.append(crud.edit_user_by_email(db, user_request, email))
    if user_id==None and username==None and email==None:
        return {"error":"No record found!!!"}
    return user

@app.get('/admin/user/delete')
def deleteUserAdmin(request:Request, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        if not crud.checkAdmin(token, db):
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    user_id = request.query_params.get('user_id', None)
    username = request.query_params.get('username', None)
    email = request.query_params.get('email', None)
    user=list()
    if user_id!= None:
        user.append(crud.delete_user_by_Id(db,user_id))
    if username!= None:
        user.append(crud.delete_user_by_username(db,username))
    if email!= None:
        user.append(crud.delete_user_by_email(db,email))
    if user_id== None and username== None and email== None:
        user.append(crud.delete_all_user(db))
    return user

@app.get('/admin/address')
def showAddressAdmin(request:Request, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        if not crud.checkAdmin(token, db):
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    user_id = request.query_params.get('user_id', None)
    id = request.query_params.get('id', None)
    distance = request.query_params.get('distance', None)
    latitude = request.query_params.get('latitude', None)
    longitude = request.query_params.get('longitude', None)
    street = request.query_params.get('street', None)
    state = request.query_params.get('state', None)
    city = request.query_params.get('city', None)
    pincode = request.query_params.get('pincode', None)
    addresstype = request.query_params.get('addresstype', None)
    address=crud.get_address(db, user_id=user_id, id=id, distance=distance, latitude=latitude, longitude=longitude, street=street, state=state, city=city, pincode=pincode, addresstype=addresstype)
    return {"address":address}

@app.get('/admin/address/add')
def addAddressAdmin(request:Request, address_request:schemas.AddressCreate, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        if not crud.checkAdmin(token, db):
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    user_id = request.query_params.get('user_id', 0)
    address=crud.create_address(db, address_request, user_id)
    return address

@app.get('/admin/address/edit')
def editAddressAdmin(request:Request, address_request:schemas.AddressCreate, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        if not crud.checkAdmin(token, db):
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    id = request.query_params.get('id', None)
    if id!=None:
        address=crud.edit_address(db, address_request, id)
    else:
        return {"error":"No recode found!!!"}
    return address

@app.get('/admin/address/delete')
def deleteAddressAdmin(request:Request, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        if not crud.checkAdmin(token, db):
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    user_id = request.query_params.get('user_id', None)
    id = request.query_params.get('id', None)
    address=list()
    if user_id!= None and id!=None:
        address.append(crud.delete_address_by_addressId(db,int(id)))
        address.append(crud.delete_address_by_userId(db,int(user_id)))
    elif user_id== None and id!=None:
        address=crud.delete_address_by_addressId(db,int(id))
    elif user_id!= None and id==None:
        address=crud.delete_address_by_userId(db,int(user_id))
    else:
        address=crud.delete_all_address(db)
    return address

#-------------------for normal users-------------------------
@app.get('/user')
def showUser(request:Request, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        user_id=crud.checkUser(token, db)
        if user_id==None :
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    if user_id!= None :
        user=crud.get_user(db,int(user_id))
    else:
        return {"error":"No User found!!!"}
    return {"user":user}

@app.get('/user/add')
def addUser(request:Request, user_request:schemas.UserCreate, db: Session = Depends(get_db)):
    user=crud.create_user(db,user_request)
    return user

@app.get('/user/edit')
def editUser(request:Request, user_request:schemas.UserEdit, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        user_id=crud.checkUser(token, db)
        if user_id==None :
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    if user_id!=None:
        user=crud.edit_user_by_token(db, user_request, token)
    else:
        return {"error":"No User found!!!"}
    return user

@app.get('/user/delete')
def deleteUser(request:Request, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        user_id=crud.checkUser(token, db)
        if user_id==None :
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    if user_id!= None:
        user=crud.delete_user_by_Id(db,user_id)
    else:
        return {"error":"No User found!!!"}
    return user


@app.get('/address')
def showAddress(request:Request, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        user_id=crud.checkUser(token, db)
        if user_id==None :
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    id = request.query_params.get('id', None)
    distance = request.query_params.get('distance', None)
    latitude = request.query_params.get('latitude', None)
    longitude = request.query_params.get('longitude', None)
    street = request.query_params.get('street', None)
    state = request.query_params.get('state', None)
    city = request.query_params.get('city', None)
    pincode = request.query_params.get('pincode', None)
    addresstype = request.query_params.get('addresstype', None)
    if user_id!= None:
        address=crud.get_address(db, user_id=user_id, id=id, distance=distance, latitude=latitude, longitude=longitude, street=street, state=state, city=city, pincode=pincode, addresstype=addresstype)
    else:
        return {"error":"No Address found!!!"}
    return {"address":address}

@app.get('/address/add')
def addAddress(request:Request, address_request:schemas.AddressCreate, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        user_id=crud.checkUser(token, db)
        if user_id==None :
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    address=crud.create_address(db, address_request, user_id=user_id)
    return address

@app.get('/address/edit')
def editAddress(request:Request, address_request:schemas.AddressCreate, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        user_id=crud.checkUser(token, db)
        if user_id==None :
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    id = request.query_params.get('id', None)
    if id!=None:
        address=crud.edit_user_address(db, address_request, id=id, user_id=user_id)
    else:
        return {"error":"No Address found!!!"}
    return address

@app.get('/address/delete')
def deleteAddress(request:Request, db: Session = Depends(get_db)):
    try:
        token=request.headers["Authorization"]
        user_id=crud.checkUser(token, db)
        print(user_id)
        if user_id==None :
            raise HTTPException(status_code=401,detail="Unauthorized")
    except:
        raise HTTPException(status_code=401,detail="Unauthorized")
    id = request.query_params.get('id', None)
    if user_id!= None and id!=None:
        address=crud.delete_user_address(db,id=id,user_id=user_id)
    else:
        return {"error":"No Address found!!!"}
    return address

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
