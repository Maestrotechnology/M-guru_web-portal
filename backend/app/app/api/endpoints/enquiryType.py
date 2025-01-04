from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from pydantic import EmailStr
from api.deps import get_db,authenticate,get_by_user,get_user_token,phoneNo_validation

router = APIRouter()

@router.post("/create_enquiryType")
async def create_enquiryType(db:Session=Depends(get_db),
                     token:str = Form(...),
                     name:str = Form(...)):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_EnquiryType=db.query(EnquiryType).filter(EnquiryType.status==1,EnquiryType.name==name).first()
    if  get_EnquiryType:
        return {"status":0,"msg":"Name Already exit"}
    addEnquiry=  EnquiryType(
                    name=name,
                    created_at = datetime.now(),
                    status =1,
                    created_by = user.id,
                    )
    db.add(addEnquiry)
    db.commit()
    return {
        "status" : 1,
        "msg":"Enquiry Type created successfully"
    }

@router.post("/update_Enquiry")
async def updateEnquiry(db:Session=Depends(get_db),
                     token:str = Form(...),
                     EnquiryType_id:int = Form(...),
                     name:str = Form(None),
                     ):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    check_Enquiry=db.query(EnquiryType).filter(EnquiryType.status==1)
    get_Enquiry=check_Enquiry.query(EnquiryType).filter(EnquiryType.id==EnquiryType_id).first()
    if not get_Enquiry:
        return {"status":0,"msg":"Enquiry Type Id not found"}
    if name:
        if check_Enquiry.filter(EnquiryType.id!=EnquiryType_id,EnquiryType.name==name).first():
            return {"status":0,"msg":"Name is already exist"}

    get_Enquiry.name=name
    get_Enquiry.updated_at=datetime.now()
    db.commit()
    return {
        "status" : 1,
        "msg":"Enquiry Updated successfully"
    }

@router.post("/delete_Enquiry")
async def deleteEnquiry(db:Session=Depends(get_db),
                     token:str = Form(...),
                     EnquiryType_id:int = Form(...) ):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_Enquiry=db.query(EnquiryType).filter(EnquiryType.id==EnquiryType_id,EnquiryType.status==1).first()
    if not get_Enquiry:
        return {"status":0,"msg":"Enquiry Type Id not found"}
    get_Enquiry.status=-1
    db.commit()
    return {
        "status" : 1,
        "msg":"EnquiryType deleted successfully"
    }

@router.post("/list_Enquiry")
async def listEnquiry(db:Session=Depends(deps.get_db),
                   token:str=Form(...),page:int=1,
                   size:int=10,
                   Enquiry_name:str=Form(None),
                   ):
    user=deps.get_user_token(db=db,token=token)
    if user:
        getEnquiry =  db.query(EnquiryType).filter(EnquiryType.status ==1)
        if Enquiry_name:
            getEnquiry = getEnquiry.filter(EnquiryType.name.like("%"+Enquiry_name+"%"))
        getEnquiry = getEnquiry.order_by(EnquiryType.id.desc())
        totalCount= getEnquiry.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        getEnquiry=getEnquiry.limit(limit).offset(offset).all()
        dataList =[]

        for row in getEnquiry:
            dataList.append({
                "EnquiryType_id" :row.id,
                "EnquiryType_name":row.name.capitalize(),
                "created_at":row.created_at,
            
            })
        data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":dataList})
        return {"status":1,"msg":"Success","data":data}
    

    else:
        return({'status' :-1,
                'msg' :'Sorry! your login session expired. please login again.'}) 
    







