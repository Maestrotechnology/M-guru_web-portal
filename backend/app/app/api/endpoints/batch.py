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

@router.post("/create_batch")
async def createBatch(db:Session=Depends(get_db),
                     token:str = Form(...),
                     name:str = Form(...),
                     start_date:datetime=Form(...),
                     end_date:datetime=Form(...),
                     fee:int=Form(...),
                     description:int=Form(None)):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_batch=db.query(Batch).filter(Batch.status==1,Batch.name==name).first()
    if  get_batch:
        return {"status":0,"msg":"Batch  Name Already exit"}
    addBatch =  Batch(
                    name=name,
                    start_date = start_date,
                    end_date=end_date,
                    fee=fee,
                    description=description,
                    created_at = datetime.now(),
                    status =1,
                    )
    db.add(addBatch)
    db.commit()
    return {
        "status" : 1,
        "msg":"Batch created successfully"
    }

@router.post("/update_batch")
async def updateBatch(db:Session=Depends(get_db),
                     token:str = Form(...),
                     batch_id:int = Form(...),
                     name:str = Form(None),
                     start_date:datetime=Form(None),
                     end_date:datetime=Form(None),
                     fee:int=Form(None),
                     ):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    check_batch=db.query(Batch).filter(Batch.status==1)
    get_batch=check_batch.query(Batch).filter(Batch.id==batch_id).first()
    if not get_batch:
        return {"status":0,"msg":"Batch Id not found"}
    if name:
        if check_batch.filter(Batch.id!=batch_id,Batch.name==name).first():
            return {"status":0,"msg":"Given Batch Name is already exist"}

    get_batch.name=name
    get_batch.start_date=start_date
    get_batch.end_date=end_date
    get_batch.fee=fee
    get_batch.updated_at=datetime.now()
    db.commit()
    return {
        "status" : 1,
        "msg":"Batch Updated successfully"
    }

@router.post("/delete_batch")
async def deleteBatch(db:Session=Depends(get_db),
                     token:str = Form(...),
                     batch_id:int = Form(...) ):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_batch=db.query(Batch).filter(Batch.id==batch_id,Batch.status==1).first()
    if not get_batch:
        return {"status":0,"msg":"Batch Id not found"}
    get_batch.status=-1
    db.commit()
    return {
        "status" : 1,
        "msg":"Batch deleted successfully"
    }

@router.post("/list_batch")
async def listBatch(db:Session=Depends(deps.get_db),
                   token:str=Form(...),page:int=1,
                   size:int=10,
                   Batch_name:str=Form(None),
                   ):
    user=deps.get_user_token(db=db,token=token)
    if user:
        getBatch =  db.query(Batch).filter(Batch.status ==1)
        if Batch_name:
            getBatch = getBatch.filter(Batch.name.like("%"+Batch_name+"%"))
        getBatch = getBatch.order_by(User.id.desc())
        totalCount= getBatch.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        getBatch=getBatch.limit(limit).offset(offset).all()
        dataList =[]

        for row in getBatch:
            dataList.append({
                "Batch_id" :row.id,
                "Batch_name":row.name,
                "start_date":row.start_date,
                "end_date":row.end_date,
                "fee":row.fee
            })
        data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":dataList})
        return {"status":1,"msg":"Success","data":data}
    

    else:
        return({'status' :-1,
                'msg' :'Sorry! your login session expired. please login again.'}) 
    







