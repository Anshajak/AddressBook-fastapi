from sqlalchemy.orm import Session
import models, schemas
import math as Math
import string, random

#-------------- user control------------
def password_hasher(password):
    fake_hashed_password = password + "notreallyhashed"
    return fake_hashed_password
def checkUser(token,db: Session):
    db_user=db.query(models.User).filter(models.User.token==token).first()
    if db_user!=None:
        return db_user.id
    return None
def checkAdmin(token,db: Session):
    db_user=db.query(models.User).filter(models.User.token==token, models.User.is_admin==True).first()
    if db_user!=None:
        return True
    return False

#-------------- fetch APIs------------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def login_user(db: Session, password: str, username: str|None=None, email: str|None=None):
    if username!=None:
        db_user=db.query(models.User).filter(models.User.username == username, models.User.password == password_hasher(user.password)).first()
        if db_user!=None:
            return {"token":db_user.token}
    if email!=None:
        db_user=db.query(models.User).filter(models.User.email == email, models.User.password == password_hasher(user.password)).first()
        if db_user!=None:
            return {"token":db_user.token}
    return False


def get_address(db: Session, skip: int = 0, limit: int = 100, user_id:str|None=None, id:str|None=None, distance:str|None=None, latitude:str|None =None, longitude:str|None =None, street:str|None =None, state:str|None =None, city:str|None =None, pincode:str|None =None, addresstype:str|None =None ):
    col=""
    filters=" where"
    order=""
    if user_id!=None:
        filters+=" and owner_id == %s"%(user_id)
    if id!=None:
        filters+=" and id == %s"%(id)
    if distance!=None:
        coef = float(distance) / 111.32
        new_lat = float(latitude) + coef
        new_long = float(longitude) + coef / Math.cos(float(latitude) * 0.01745)
        col = ", (6367*acos(cos(radians(%2f))*cos(radians(latitude))*cos(radians(longitude)-radians(%2f))+sin(radians(%2f))*sin(radians(latitude)))) as distance"% (float(new_lat),float(new_long),float(new_lat))
        filters+= " distance <= %2f" %(coef)
        order=" ORDER BY distance"
    if latitude!=None and distance==None:
        filters+=" and latitude == %s"%(latitude)
    if longitude!=None and distance==None:
        filters+=" and longitude == %s"%(longitude)
    if street!=None:
        filters+=" and street == '%s'"%(street)
    if state!=None:
        filters+=" and state == '%s'"%(state)
    if city!=None:
        filters+=" and city == '%s'"%(city)
    if pincode!=None:
        filters+=" and pincode == '%s'"%(pincode)
    if addresstype!=None:
        filters+=" and addresstype == '%s'"%(addresstype)
    if len(filters)<7:
        filters=""
    else:
        if filters[6:10]==" and":
            filters=filters[:6]+filters[10:]
    query = "SELECT * %s FROM address %s %s"%(col,filters,order)
    return db.execute(query).all()

#-------------- create APIs------------
def create_user(db: Session, user: schemas.UserCreate):
    token=''.join(random.choices(string.ascii_uppercase+ string.digits + string.ascii_lowercase, k=35 ))
    while 1:
        if db.query(models.User).filter(models.User.token == str(token)).first():
            token=''.join(random.choices(string.ascii_uppercase+ string.digits + string.ascii_lowercase, k=35 ))
        else:
            break
    try:
        db_user = models.User(email=user.email, username=user.username, hashed_password=password_hasher(user.password), token=str(token))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except:
        return {"error_code":"Unique key error","error":'User with username or Email is already exist'}
    return {"token":db_user.token}

def create_admin(db: Session, user: schemas.AdminCreate):
    token=''.join(random.choices(string.ascii_uppercase+ string.digits + string.ascii_lowercase, k=35 ))
    while 1:
        if db.query(models.User).filter(models.User.token == str(token)).first():
            token=''.join(random.choices(string.ascii_uppercase+ string.digits + string.ascii_lowercase, k=35 ))
        else:
            break
    try:
        db_user = models.User(email=user.email, username=user.username, is_active=user.is_active, is_admin=user.is_admin, hashed_password=password_hasher(user.password), token=str(token))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except:
        return {"error_code":"Unique key error","error":'User with username or Email is already exist'}
    return {"token":db_user.token}

def create_address(db: Session, address: schemas.AddressCreate, user_id: int):
    db_address = models.Address(**address.dict(), owner_id=user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return {"msg":"New address created!!","result":db_address}


#-------------- update APIs------------

def edit_user_by_Id(db: Session, user: schemas.UserEdit, id: int):
    try:
        db_user=db.query(models.User).filter(models.User.id == id).update({
            'email':user.email,
            'username':user.username,
            'is_admin':user.is_admin,
            'is_active':user.is_active,
            'hashed_password':password_hasher(user.password)})
    except:
        return {"error":"No recode found!!!"}
    db.commit()
    return {"result":"Udated user of user of id: "+id}

def edit_user_by_username(db: Session, user: schemas.UserEdit, username: str):
    try:
        db_user=db.query(models.User).filter(models.User.username == username).update({
            'email':user.email,
            'username':user.username,
            'is_admin':user.is_admin,
            'is_active':user.is_active,
            'hashed_password':password_hasher(user.password)})
    except:
        return {"error":"No recode found!!!"}
    db.commit()
    return {"result":"Udated user of user of username: "+username}

def edit_user_by_email(db: Session, user: schemas.UserEdit, email: str):
    try:
        db_user=db.query(models.User).filter(models.User.email == email).update({
            'email':user.email,
            'username':user.username,
            'is_admin':user.is_admin,
            'is_active':user.is_active,
            'hashed_password':password_hasher(user.password)})
    except:
        return {"error":"No recode found!!!"}
    db.commit()
    return {"result":"Udated user of user of email: "+email}

def edit_user_by_token(db: Session, user: schemas.UserEdit, token: str):
    try:
        db_user=db.query(models.User).filter(models.User.token == token).update({'hashed_password':password_hasher(user.password)})
    except:
        return {"error":"No recode found!!!"}
    db.commit()
    return {"result":"Udated password of user of token: "+token}

def edit_address(db: Session, address: schemas.AddressCreate, id: int):
    try:
        db_address=db.query(models.Address).filter(models.Address.id == id).update({
            "latitude":address.latitude,
            "longitude":address.longitude,
            "street":address.street,
            "city":address.city,
            "state":address.state,
            "pincode":address.pincode,
            "addresstype":address.addresstype
        })
    except:
        return {"error":"No recode found!!!"}
    db.commit()
    db_address=db.query(models.Address).filter(models.Address.id == id).first()
    return {"msg":"editd address of id: "+id,"result":db_address}

def edit_user_address(db: Session, address: schemas.AddressCreate, id: str, user_id: str):
    try:
        db_address=db.query(models.Address).filter(models.Address.id == id,models.Address.owner_id == user_id).update({
            "latitude":address.latitude,
            "longitude":address.longitude,
            "street":address.street,
            "city":address.city,
            "state":address.state,
            "pincode":address.pincode,
            "addresstype":address.addresstype
        })
        #Ansh@j
    except:
        return {"error":"No recode found!!!"}
    db.commit()
    db_address=db.query(models.Address).filter(models.Address.id == id,models.Address.owner_id == user_id).first()
    return {"msg":"editd address of id: "+id,"result":db_address}


#-------------- delete APIs------------
def delete_all_user(db: Session,):
    db_user=db.query(models.User).all()
    if db_user==None:
        return {"error":"No recode found!!!"}
    db.delete(db_user)
    db.commit()
    return {"msg":"deleted all"}

def delete_user_by_Id(db: Session, id: str):
    db_user=db.query(models.User).filter(models.User.id == int(id)).first()
    if db_user==None:
        return {"error":"No recode found!!!"}
    db.delete(db_user)
    db.commit()
    return {"msg":"deleted user of id: %d"%(id)}

def delete_user_by_username(db: Session, username: str):
    db_user=db.query(models.User).filter(models.User.username == username).first()
    if db_user==None:
        return {"error":"No recode found!!!"}
    db.delete(db_user)
    db.commit()
    return {"msg":"deleted user of username: "+username}

def delete_user_by_email(db: Session, email: str):
    db_user=db.query(models.User).filter(models.User.email == email).first()
    if db_user==None:
        return {"error":"No recode found!!!"}
    db.delete(db_user)
    db.commit()
    return {"msg":"deleted user of email: "+email}


def delete_all_address(db: Session,):
    db_address=db.query(models.Address).all()
    if db_address==None:
        return {"error":"No recode found!!!"}
    db.delete(db_address)
    db.commit()
    return {"msg":"deleted all"}

def delete_address_by_addressId(db: Session, id: str):
    db_address=db.query(models.Address).filter(models.Address.id == int(id)).first()
    if db_address==None:
        return {"error":"No recode found!!!"}
    db.delete(db_address)
    db.commit()
    return {"msg":"deleted address of id: "+id}

def delete_address_by_userId(db: Session, user_id: str):
    db_address=db.query(models.Address).filter(models.Address.owner_id == int(user_id))
    if db_address==None:
        return {"error":"No recode found!!!"}
    db.delete(db_address)
    db.commit()
    return {"msg":"deleted all addresses of userid: "+user_id}

def delete_user_address(db: Session, id: str, user_id: str):
    db_address=db.query(models.Address).filter(models.Address.owner_id == int(user_id),models.Address.id == int(id)).first()
    if db_address==None:
        return {"error":"No recode found!!!"}
    db.delete(db_address)
    db.commit()
    return {"msg":"deleted address of id: "+id}
