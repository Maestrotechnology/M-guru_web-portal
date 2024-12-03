
from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_,cast,Date
import random
router = APIRouter()
dt = str(int(datetime.utcnow().timestamp()))

#Check Token
@router.post("/check_token")
async def checkToken(*,db: Session = Depends(deps.get_db),
                      token: str = Form(...)):
    
    checkToken = db.query(ApiTokens).filter(ApiTokens.token == token,
                                           ApiTokens.status == 1).first()
    if checkToken:
        return {"status":1,"msg":"Success."}
    else:
        return {"status":0,"msg":"Failed."}


#1.Login
@router.post("/login")
async def login(*,db: Session = Depends(deps.get_db),
                authcode: str = Form(None),
                userName: str = Form(...),
                password: str = Form(...)
                ,device_id: str = Form(None),
                device_type: str = Form(...,description = "1-android,2-ios"),
                push_id: str = Form(None),
                ip: str = Form(None),resetKey: str = Form(None),
                otp: str = Form(None)):
    
    ip = ip
    if device_id:
        auth_text = device_id + str(userName)
    else:
        auth_text = userName
    
    user = deps.authenticate(db,username = userName,
                             password = password,
                           authcode = authcode,
                           auth_text = auth_text)
  
    if not user:
        return {"status": 0,"msg": "Invalid username or password."}
    
    else:
        key = None
        userId = user.id

        if otp:
            user.otp = otp
            user.reset_key = resetKey
            msg = f"YOUR OTP IS {otp}"
            send = await send_mail(receiver_email = user.email,
                                 message = msg)
            db.commit()
    
        else:
            
            key = ''
            char1 = '0123456789abcdefghijklmnopqrstuvwxyz'
            char2 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            characters = char1 + char2
            token_text = userId
            for i in range(0, 30):
                key += characters[random.randint(
                        0, len(characters) - 1)]
                
            # delToken = db.query(ApiTokens).\
            #     filter(ApiTokens.user_id == user.id).update({'status': 0})

            addToken = ApiTokens(user_id = userId,
                                token = key,
                                created_at = datetime.now(settings.tz_IN),
                                renewed_at = datetime.now(settings.tz_IN),
                                validity = 1,
                                device_type = device_type,
                                device_id = device_id,
                                push_device_id = push_id,
                                device_ip = ip,
                                status = 1)
                    

            db.add(addToken)
            db.commit()
            checkTodayCheckIN = (
            db.query(Attendance)
            .filter(
                Attendance.user_id == user.id,
                cast(Attendance.check_in, Date) == datetime.now(settings.tz_IN).date(),
            )
            .first()
        )
            return {'status':1,
                'token': key,
                "user_id":user.id,
                "user_type":user.user_type,
                'msg': 'Successfully LoggedIn.',  
                'status': 1,
                "checkin_time":checkTodayCheckIN.check_in if checkTodayCheckIN else None
                }

        
    
    
#2.Logout
@router.post("/logout")
async def logout(db: Session = Depends(deps.get_db),
                 token: str = Form(...)):

    user = deps.get_user_token(db = db,token = token)
    if user:
        check_token = db.query(ApiTokens).\
            filter(ApiTokens.token == token,ApiTokens.status == 1).first()

        if check_token:
            check_token.status = -1
            db.commit()
            return ({"status": 1,"msg": "Success."}) 
        else:
            return ({"status": 0,"msg": "Failed."})
    else:
        return ({"status":0,"msg":"Invalid user."})
    

#3.Otp Verification
"""After the Successful SignIn Then You want to Verify
so An otp is sended to your register then u want to verify here"""

# @router.post("/otpVerification")

# async def otpVerification(*,db: Session = Depends(deps.get_db),
#                            otp: str = Form(...),
#                            reset_key: str = Form(...),
#                            verificationType:str=Form(None,
#                             description="1->credentials")):

#     checkUser=db.query(User).\
#         filter(User.status == 1,User.reset_key == reset_key).first()
#     if checkUser:
#         if otp == checkUser.otp:
#             if checkUser.otp_verified_at <= datetime.now():

#                 checkUser.otp_verified = 1
#                 checkUser.reset_key = None
#                 checkUser.otp = None
#                 db.commit()
#                 if verificationType != str(2):
#                     if not verificationType:
#                         msg = f"Subject: Welcome\n\n YOU ARE VERIFIED"
#                     elif verificationType == str(1):
#                         msg = f"Subject: Welcome Back\n\n YOUR USER NAME IS :{checkUser.name}"
                

#                     try:
#                         send = await send_mail(
#                             receiver_email = checkUser.email,
#                             message = msg)
#                     except:
#                         return ({"status": 0,
#                                 "msg": "Can't connect to server . Try later."})
#                 return ({"status": 1,
#                         "msg": "Credential send to your email or mobile number."})
               
#             else:
#                 return {"status": 0,"msg": "Time out."}
#         else:
#             return {"status": 0,"msg": "Otp not match."}
#     else:
#         return {"status": 0,"msg": "No user found."}
    

@router.post("/verify_otp")
async def verifyOtp(db:Session = Depends(deps.get_db),
                    resetKey:str= Form(...),otp:str=Form(...)):
    
    getUser = db.query(User).filter(User.reset_key == resetKey,
                                    User.status == 1).first()
    
    if getUser:
        if getUser.otp == str(otp):
            
            if getUser.otpExpireAt >= datetime.now(settings.tz_IN).replace(tzinfo=None):
                getUser.otp = None
                getUser.otpExpireAt = None
        
                (otp, reset, created_at,
                    expire_time, expire_at,
                        otp_valid_upto) = deps.get_otp()
                
                reset_key = f'{reset}{getUser.id}DTEKRNSSHPT'
                getUser.reset_key = reset_key
                
                db.commit()
                return {"status":1,"msg":"Verified.","reset_key":reset_key}
            
            else:
                return ({"status": 0,"msg": "time out."})
        else:
            return ({"status": 0,"msg": "otp not match."})
    else:
        return {"status":0,"msg":"No record found."}
     

#4.change Password
""" This Api is for that Exception Case thus the User
Wants to Change their Password"""

@router.post("/changePassword")

async def changePassword(db: Session = Depends(deps.get_db),
                          token: str = Form(...)
                          ,old_password: str = Form(None),
                          new_password: str = Form(...),
                          repeat_password: str = Form(...)):

    user = deps.get_user_token(db = db,token = token)
    if user:
        
        
        if  verify_password(old_password,user.password):

            if new_password!=repeat_password:
                return ({"status":0,"msg":"Password is not match."})
            
            else:           
                user.password = get_password_hash(new_password)
                db.commit()

                return ({"status": 1,"msg": "Password successfully updated."})
        else:
            return ({"status": 0,"msg": "Current password is invalid."})
    else:  
        return ({"status":-1,"msg":"Login session expires"})
    
#5.reSendOtp
@router.post("/resendOtp")
async def resendOtp(db: Session = Depends(deps.get_db),
                     resetKey: str = Form(...)):

    getUser = db.query(User).\
        filter(User.reset_key == resetKey,User.status == 1).first()
    
    if getUser:
        (otp, reset,
         created_at, 
         expireTime, 
         expireAt, otpValidUpto) = deps.get_otp()
        resetKey = reset+"@ghgkhdfkjh@trhghgu"
        otp = "123456"
        getUser.otp = otp
        getUser.reset_key = resetKey
        getUser.otpExpireAt = expireAt
        db.commit()

        msg=f"THANKS FOR CHOOSING OUR SERVICE YOUR SIX DIGIT OTP PIN IS {otp}"
        try:
            send = await send_mail(receiver_email = getUser.email,message = msg)
            return ({"status": 1,"msg": "OTP sended to your email",
                 "reset_key": resetKey,
                 "remaining_seconds": 120})
        except:
            return {"status":0,"msg":"Email not proper."}
        
    return ({"status": 0,"msg": "Non User Found"})


# 6. FORGOT PASSWORD

@router.post('/forgotPassword')
async def forgotPassword(db: Session = Depends(deps.get_db),    
                                    email: str = Form(None)):
    
    user = db.query(User).filter(
                                 or_(User.email==email,
                                     User.phone==email,
                                     ),
                                  User.status == 1)
    checkUser = user.first()
    if checkUser:
        
        if checkUser.email :
            (otp, reset, created_at,
            expire_time, expire_at,
                otp_valid_upto) = deps.get_otp()
        
            otp="123456"
            message = f'''Your  OTP for Reset Password is : {otp}'''
            reset_key = f'{reset}{checkUser.id}DTEKRNSSHPT'
            print(datetime.now())
    
            user = user.update({'otp': otp,
                                'reset_key': reset_key,
                                'otpExpireAt': expire_at})
            db.commit()

            # mblNo = f'+91{checkUser.mobile}'
            try:
                send = await send_mail(receiver_email = checkUser.email,message = message)
                # print(message)
                return ({'status':1,'reset_key': reset_key,
                        'msg': 
                        f'An OTP message has been sent to {checkUser.email}.',
                        'remaining_seconds':120})
            except Exception as e:
                # print("EXCEPTION: ",e)
                return {'status':0,'msg':'Unable to send the Email.'}

        else:
            return({'status': 0,
    'msg': "Email address not found. Contact administrator for assistance."} )

    else:
        return({'status':0,'msg':'Sorry. The requested account not found'})
    
@router.post("/reset_password")
async def resetPassword(db:Session=Depends(deps.get_db),
                         resetKey:str = Form(...),
                         newPassword:str = Form(...)):
    getUser = db.query(User).filter(User.reset_key == resetKey,
                                    User.status == 1).first()
    if getUser:
        
        getUser.password = get_password_hash(newPassword)
        getUser.reset_key = None
        db.commit()
        return {"status":1,"msg":"Password changed successfully."}
    else:
        return {"status":-1,"msg":"You cannot change the password at this moment.Please try later."}
    

@router.post("/changeUserPassword")

async def changeUserPassword(db: Session = Depends(deps.get_db),
                          token: str = Form(...),
                          
                          new_password: str = Form(...),
                          confirm_password: str = Form(...),
                          userId:int=Form(...)):

    user = deps.get_user_token(db = db,token = token)
    if user:
        
        
        get_user=db.query(User).filter(User.id==userId,User.status==1).first()
        if not get_user:
            return ({"status":0,"msg":"user not Found"})



        if new_password!=confirm_password:
            return ({"status":0,"msg":"Password is not match."})
        
        else:           
            get_user.password = get_password_hash(new_password)
            db.commit()

            return ({"status": 1,"msg": "Password successfully updated."})
        
    else:  
        return ({"status":-1,"msg":"Login session expires"})
    
# @router.post("/signupUser")
# async def signupUser(db: Session = Depends(deps.get_db),
#                       name: str = Form(...),
#                       email: str = Form(...),
#                       mobileNumber: str = Form(...),
#                       alternativeNumber: str = Form(None),
#                       password: str = Form(...)):

#     getUser = db.query(User).filter(User.status==1,User.otpVerifiedStatus==1)
        
#     if mobileNumber:
#             checkMobileNumber = getUser.\
#                 filter(or_(User.phone == mobileNumber,
#                         User.alternativeNumber == mobileNumber))
    
#             if checkMobileNumber:
#                 return {"status": 0,"msg": "Mobile number already exists."}
                
#     if alternativeNumber and mobileNumber :

#         if alternativeNumber == mobileNumber:
#                 return {"status": 0,
#                         "msg": ("Mobile number and alternative mobile number are same.")}
#         else:
#             checkAlternativeNumber = getUser.\
#                 filter(or_(User.phone == alternativeNumber,
#                        User.alternativeNumber == mobileNumber))
            
#             if checkAlternativeNumber:
#                 return {"status": 0,"msg": "Mobile number already exists!"}
            
#         if email:
#             getEmail = getUser.\
#                 filter(User.email == email).first()
#             if getEmail:
#                 return {"status": 0,
#                         "msg": "Email already exist!"}
        
#         alternative_mobile_no = (alternative_mobile_no 
#                                if alternative_mobile_no else None)
#         pwd=password
#         if pwd:
#             password = get_password_hash(pwd)
#         else:
#             return {"status": 0,"msg": "Password not matched!"}
        

#         (otp, reset, created_at,
#           expire_time, expire_at,
#             otp_valid_upto) = deps.get_otp()
        
#         otp = "123456"
#         reset_key1 = f'{reset}TnrTkd10jf1998J7u20I@'
  
#         msg = f"Subject: Welcome to Mconnect Family\n\n Your otp  is {otp}   Stay Connected With MConnect."
#         send = await send_mail(receiver_email=email,message=msg)
        
#         createUser = User(email=email,
#                           userType=1,
#                           name=name,
#                         phone=mobileNumber,
#                         alternativeNumber=alternativeNumber,
#                         contact_person=name,
#                         created_at=datetime.now(settings.tz_IN),
#                         status=1,password=password,
#                         otp=otp,
#                         otpVerifiedStatus=0,otpExpireAt=expire_at,
#                         reset_key=reset_key1)

#         db.add(createUser)
#         db.commit()  


#         return ({"status":1,"reset_key":reset_key1,
#                  "duration":120,
#                  "msg":f"An OTP message has been sent to {email}"})

import hashlib
@router.post("/getAuth")
async def getAuth(name:str=Form(...)):
    
    salt = settings.SALT_KEY
    name = salt+name
    
    result = hashlib.sha1(name.encode())
    
    print(result.hexdigest())
    return result.hexdigest()

# @router.post('/forgotPassword')
# async def forgotPassword(db: Session = Depends(deps.get_db),    
#                                     email: str = Form(None)):
#     userTypeData = [1,2,3,4]
#     user = db.query(User).filter(User.userType.in_(userTypeData),
#                                  User.email == email,
#                                   User.status == 1)
#     checkUser = user.first()
#     if checkUser:
        
#         (otp, reset, created_at,
#         expire_time, expire_at,
#             otp_valid_upto) = deps.get_otp()
    
#         otp="123456"
#         message = f'''Your OTP for Reset Password is : {otp}'''
#         reset_key = f'{reset}{checkUser.id}DTEKRNSSHPT'

#         user = user.update({'otp': otp,
#                             'reset_key': reset_key,
#                             'otpExpireAt': expire_at})
#         db.commit()

#         try:
#             send = await send_mail(receiver_email = checkUser.email,
#                                     message = message)
#             return ({'status': 1,'reset_key': reset_key,
#                     'msg': 
#                     f'An OTP message has been sent to {email}.',
#                     'remaining_seconds': otp_valid_upto})
        
#         except Exception as e:
#             print("EXCEPTION: ",e)
#             return {'status': 0,'msg': 'Unable to send the Email.'}


#     else:
#         return({'status':0,'msg':'Sorry. The requested account not found'})


# @router.post('/forgotPassword')
# async def forgotPassword(db: Session = Depends(deps.get_db),    
#                                     email: str = Form(None)):
    
#     user = db.query(User).filter( User.email == email,
#                                   User.status == 1)
#     checkUser = user.first()
#     if checkUser:
#         if checkUser.is_active ==0:
#             return {"status":0,
#                     "msg":
#                     "Access denied. Your account is inactive. Contact admin for further assistance."}
        
#         else:
 
#             (otp, reset, created_at,
#             expire_time, expire_at,
#                 otp_valid_upto) = deps.get_otp()
        
#             otp="123456"
#             message = f''' OTP for forgetting your password is: {otp}'''
#             reset_key = f'{reset}{checkUser.id}DTEKRNSSHPT'
    
#             user = user.update({'otp': otp,
#                                 'reset_key': reset_key,
#                                 'otp_expire_at': expire_at})
#             db.commit()
 
#             try:
#                 async def send_mail(receiver_email, message):  # Demo
#                     sender_email = "maestronithishraj@gmail.com"
#                     receiver_email = receiver_email
#                     password = "ycjanameheveewtb"
                
#                     msg = message
                
#                     server = smtplib.SMTP("smtp.gmail.com", 587)
#                     server.ehlo()
#                     server.starttls()
#                     server.login(sender_email, password)
#                     server.sendmail(sender_email, receiver_email, msg)
#                     server.quit()
                
#                     return True
#                 send = await send_mail_req_approval(db,email_type=4,article_id=None,user_id=checkUser.id,
#                                                     subject="Forget Password",
#                                                     journalistName=checkUser.name,
#                                                     receiver_email = checkUser.email,
#                                        message = message)
#                 return ({'status': 1,'reset_key': reset_key,
#                         'msg':
#                         f'An OTP message has been sent to {email}.',
#                         'remaining_seconds': otp_valid_upto})
            
#             except Exception as e:
#                 print("EXCEPTION: ",e)
#                 return {'status': 0,'msg': 'Unable to send the Email.'}
 
 
#     else:
#         return({'status':0,'msg':'Sorry. The requested account not found'})
    
# @router.post("/verify_otp")
# async def verifyOtp(db:Session = Depends(deps.get_db),
#                     resetKey:str= Form(...),otp:str=Form(...)):
    
#     getUser = db.query(User).filter(User.reset_key == resetKey,
#                                     User.status == 1,User.is_active==1).first()
    
#     if getUser:
#         if getUser.otp == str(otp):
#             if getUser.otp_expire_at >= datetime.now(settings.tz_IN).replace(tzinfo=None):
#                 getUser.otp = None
#                 getUser.otp_expire_at = None
        
#                 (otp, reset, created_at,
#                     expire_time, expire_at,
#                         otp_valid_upto) = deps.get_otp()
                
#                 reset_key = f'{reset}{getUser.id}DTEKRNSSHPT'
#                 getUser.reset_key = reset_key
                
#                 db.commit()
#                 return {"status":1,"msg":"Verified.","reset_key":reset_key}
            
#             else:
#                 return ({"status": 0,"msg": "time out."})
#         else:
#             return ({"status": 0,"msg": "otp not match."})
#     else:
#         return {"status":0,"msg":"No record found."}
 
# @router.post("/resend_otp")
# async def resendOtp(db:Session = Depends(deps.get_db),
#                     resetKey:str= Form(...)):
#     getUser = db.query(User).filter(User.reset_key == resetKey,
#                                     User.status == 1,User.is_active==1).first()
    
#     if getUser:
#         (otp, reset, created_at,
#             expire_time, expire_at,
#                 otp_valid_upto) = deps.get_otp()
#         otp="123456"
#         message = f'''Your OTP for Reseting your Password is : {otp}'''
#         reset_key = f'{reset}{getUser.id}DTEKRNSSHPT'
 
#         getUser.otp = otp
#         getUser.reset_key = reset_key
#         getUser.otp_expire_at = expire_at
                          
#         db.commit()
 
#         try:
#             send = await send_mail_req_approval(db,email_type=4,article_id=None,user_id=getUser.id,
#                                                     subject="Reset Password",
#                                                     journalistName=getUser.name,
#                                                     receiver_email = getUser.email,
#                                        message = message)
        
#             return ({'status': 1,'reset_key': reset_key,
#                     'msg':
#                     f'An OTP message has been sent to {getUser.email}.',
#                     'remaining_seconds': otp_valid_upto})
        
#         except Exception as e:
#             print("EXCEPTION: ",e)
#             return {'status': 0,'msg': 'Unable to send the Email.'}
#     else:
#         return {'status':0,"msg":"No user found."}
 