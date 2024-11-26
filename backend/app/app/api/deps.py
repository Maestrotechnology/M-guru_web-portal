from typing import Generator, Any, Optional
from fastapi.security import OAuth2PasswordBearer
import datetime
from sqlalchemy.orm import Session
from app import models
import random
from sqlalchemy import or_
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from datetime import datetime,timedelta
import hashlib
from app.models import ApiTokens,User
from app.core.config import settings


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_token(db: Session, *, token: str) :
    get_token=db.query(ApiTokens).filter(ApiTokens.token== token ,
                                            ApiTokens.status==1).first()

    if get_token: 
        return db.query(User).filter(User.id == get_token.user_id,
                                         User.status == 1).first()            
    else:
        return None


def get_by_user(db: Session, *, username: str):
        
        getUser=db.query(models.User).\
            filter( models.User.userName == username 
                   ,models.User.status == 1).first()
        return getUser


def authenticate(db: Session, *, username: str, password: str ,
                  authcode:str ,
                    auth_text:str) -> Optional[models.User]:
    
        user = get_by_user(db, username=username) 
       
        if not user or user.password == None:
           
            
            return None

        if not security.check_authcode(authcode, auth_text):
          
   
            return None

        if not security.verify_password(password, user.password):
           

            return None
        return user


def get_user_type(user_type: Any):
    if user_type == 1:
        return "Admin"

    elif user_type == 2:
        return "Customer"

    else:
        return ""

def verify_hash(hash_data:str, included_variable:str):

    included_variable = (included_variable + settings.SALT_KEY).encode("utf-8")
    real_hash = hashlib.sha1(included_variable).hexdigest()
    if hash_data == real_hash:
        return True
        
    return False

def checkSignature(signature:str, timestamp:str, device_id:str):

    included_variable = (device_id + timestamp + settings.SALT_KEY).encode("utf-8")
    real_hash = hashlib.sha1(included_variable).hexdigest()
    if signature == real_hash:
        return True
    return False


def get_otp():
    otp = ''
    reset = ""
    characters = '0123456789'
    char1 = 'qwertyuioplkjhgfdsazxcvbnm0123456789'
    char2 = 'QWERTYUIOPLKJHGFDSAZXCVBNM'
    reset_character = char1 + char2
    
    otp = random.randint(111111, 999999)
   
    for j in range(0, 20):
        reset += reset_character[random.randint(
            0, len(reset_character) - 1)]

    created_at = datetime.now(settings.tz_IN)
    expire_time = created_at +timedelta(minutes=2)
    expire_at = expire_time.strftime("%Y-%m-%d %H:%M:%S")
    otp_valid_upto = expire_time.strftime("%d-%m-%Y %I:%M %p")

    return [otp, reset , created_at, expire_time, expire_at, otp_valid_upto] 


def hms_to_s(s):
    t = 0
    for u in s.split(':'):
        t = 60 * t + int(u)
    return t

def phoneNo_validation(phonenumber:str):
    length = 10
    length_of_phonenumber =  len(phonenumber)
    if length == length_of_phonenumber:
        return True
    return False

