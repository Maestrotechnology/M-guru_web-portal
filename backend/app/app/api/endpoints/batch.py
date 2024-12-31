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
from api.deps import get_db,authenticate,get_by_user,get_user_token,phoneNo_validation,get_username
from utils import file_storage,send_mail,get_pagination
from api.endpoints.email_templetes import get_email_templete

router = APIRouter()

@router.post("/create_batch")
async def createBatch(db:Session=Depends(get_db),
                     token:str = Form(...),
                     name:str = Form(...),
                     start_date:datetime=Form(...),
                     end_date:datetime=Form(...),
                     fee:int=Form(...),
                     description:str=Form(None)
):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type !=1:
        return {"status":0,"msg":"Access denied"}
    
    get_batch=db.query(Batch).filter(Batch.status==1,Batch.name==name).first()
    if  get_batch:
        return {"status":0,"msg":"Batch  Name Already exit"}
    
    get_all_batch = db.query(Batch).filter(Batch.status != -1).update({Batch.status: 2})
    db.commit()

    addBatch =  Batch(
                    name=name,
                    start_date = start_date,
                    end_date=end_date,
                    fee=fee,
                    description=description,
                    created_at = datetime.now(),
                    status =1,
                    created_by= user.id
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
                     name:str = Form(...),
                     start_date:datetime=Form(...),
                     end_date:datetime=Form(...),
                     fee:int=Form(...),
):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type !=1:
        return {"status":0,"msg":"Access denied"}
    
    check_batch=db.query(Batch).filter(Batch.status==1)
    get_batch=check_batch.filter(Batch.id==batch_id).first()
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
                     batch_id:int = Form(...),
                     value: int = Form(...,description="1-> active , 2 -> inactive , 3-> delete") 
):
    
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type !=1:
        return {"status":0,"msg":"Access denied"}
    
    get_batch=db.query(Batch).filter(Batch.id==batch_id).first()
    if not get_batch:
        return {"status":0,"msg":"Batch Id not found"}
    if value == 3:
        get_batch.status=-1
        
    elif value == 2 or value == 1:
        get_batch.status=value

    else:
        return {"status":0,"msg":"Invalid type"}
    db.commit()
    return {
        "status" : 1,
        "msg":"Batch activated successfully" if value == 1 else "Batch inactived successfully" if value == 2 else "Batch deleted successfully"
    }

@router.post("/list_batch")
async def listBatch(db:Session=Depends(deps.get_db),
                   token:str=Form(...),page:int=1,
                   size:int=10,
                   Batch_name:str=Form(None),
                   active_inactive_batch: int = Form(None,description="1-> active , 2-> inactive")
                   ):
    user=get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type not in [1,2]:
        return {"status":0,"msg":"Access denied"}
    getBatch =  db.query(Batch).filter(Batch.status.in_([1,2]))
    if active_inactive_batch:
        getBatch =  getBatch.filter(Batch.status==active_inactive_batch)
    if Batch_name:
        getBatch = getBatch.filter(Batch.name.like("%"+Batch_name+"%"))
    getBatch = getBatch.order_by(Batch.id.desc())
    totalCount= getBatch.count()
    total_page,offset,limit=get_pagination(totalCount,page,size)
    getBatch=getBatch.limit(limit).offset(offset).all()
    dataList =[]

    for row in getBatch:
        batch_count = db.query(User).filter(User.batch_id==row.id,User.user_type==3,User.status.in_([1,2])).count()
        dataList.append({
                "Batch_id" :row.id,
                "Batch_name":row.name.capitalize(),
                "start_date":row.start_date,#.strftime("%d-%m-%Y %H:%M"),
                "end_date":row.end_date,#.strftime("%d-%m-%Y %H:%M"),
                "fee":row.fee,
                "batch_count":batch_count,
                "status": row.status
            })
    data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":dataList})
    return {"status":1,"msg":"Success","data":data}
    
        
 
    
@router.post("/allocate_batch")
async def allocateBatch(token:str=Form(...),
                        db: Session=Depends(get_db),
                        application_id: int=Form(...),
                        batch_id: int=Form(...),
                        course_id: int=Form(...),
):
    user=get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type != 1:
        return {"status":0,"msg":"Access denied"}
    
    application_data = db.query(ApplicationDetails).filter(ApplicationDetails.id == application_id,ApplicationDetails.status==1).first()
    if not application_data:
        return {"status":0, "msg":"Invalid application"}
    batch_data = db.query(Batch).filter(Batch.id == batch_id,Batch.status == 1).first()
    if not batch_data:
        return {"status":0, "msg":"Invalid batch"}
    course_data = db.query(Course).filter(Course.id == course_id,Course.status == 1).first()
    if not course_data:
        return {"status":0, "msg":"Invalid Course"}
    
    checkUser = db.query(User).filter(User.status==1)

    if checkUser.filter(User.email == application_data.email,User.batch_id==batch_id).first():
        return {"status":0,"msg":"Give Email is already exist"}
    if checkUser.filter(User.phone==application_data.phone,User.batch_id==batch_id).first():
        return {"status":0,"msg":"Given Phone Number is already exist"}
    
    # await send_mail(receiver_email=application_data.email,message=get_email_templete(application_data,batch_data.start_date,4),subject="Application status")

    create_student = User(
        name = application_data.name,
        email = application_data.email,
        user_type = 3,
        username = get_username(db,3),
        password = get_password_hash("12345"),
        create_at = datetime.now(settings.tz_IN),
        status = 1,
        phone=application_data.phone,
        batch_id = batch_id,
        course_id = course_id
    )
    application_data.batch_id = batch_id
    db.add(create_student)
    db.commit()

    return {"status":1,"msg":"Successfully sent the details to the student and allocated the batch"}

@router.post("/list_batch_details")
async def listBatchDetails(
                            db: Session=Depends(deps.get_db),
                            token:  str=Form(...),
                            batch_id: int = Form(...),
                            course_id: int = Form(None),
                            name: str = Form(None),
                            email: str = Form(None),
                            phone: str = Form(None),    
                            page:int=1,
                            size:int=50,
):
    user=get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type not in [1,2]:
        return {"status":0,"msg":"Access denied"}
        
    
    batch_data = db.query(Batch).filter(Batch.id == batch_id,Batch.status!=-1).first()
    if not batch_data:
        return {"status":0, "msg":"Invalid batch"}
    
    students = db.query(User).filter(
        User.batch_id==batch_id,User.status.in_([1,2]),User.user_type==3
    ).join(
            CourseAssign, CourseAssign.user_id == User.id)
    print(students.count(),11111111111111111)
    if user.user_type ==2:
        course_list = [course.course_id for course in db.query(CourseAssign).filter(CourseAssign.user_id == user.id, CourseAssign.status == 1).all()]
        students = students.filter(CourseAssign.course_id.in_(course_list))
    if course_id:
        students = students.filter(CourseAssign.course_id == course_id,CourseAssign.status==1)
    if name:
        students = students.filter(User.name.like(f"%{name}%"))
    if email:
        students = students.filter(User.email.like(f"%{email}%"))
    if phone:
        students = students.filter(User.phone.like(f"%{phone}%"))
    print(students.count(),222222222222222)
    students = students.order_by(User.id.desc())
    print(students.count(),333333333333)
    totalCount= students.count()

    total_page,offset,limit=get_pagination(totalCount,page,size)
    print(limit,offset)
    students=students.limit(limit).offset(offset).all()
    print(len(students))
    dataList =[]

    for student in students:
        course_data = []
        get_course = db.query(Course).join(CourseAssign,Course.id==CourseAssign.course_id).filter(CourseAssign.user_id==student.id,CourseAssign.status==1).all()
        if get_course:
            for course in get_course:
                course_data.append({
                    "Course_Id":course.id,
                    "Course_name":course.name
                })
        dataList.append({
            "id": student.id,
            "name": student.name.capitalize(),
            "email": student.email,
            "username": student.username,
            "phone": student.phone,
            "address": student.address,
            "course": course_data,
            "batch_id": batch_id,
            # "course_id": student.course_id
        })
        
    data=({"page":page,
           "size":size,
           "total_page":total_page,
            "total_count":totalCount,
            "items":dataList})
    
    return {"status":1,"msg":"Success","data":data}
    
@router.post("/list_active_branch_student")
async def listActiveBranchStudent(
                                    db: Session=Depends(get_db),
                                    token:  str=Form(...),
                                    course_id: int = Form(None),
                                    name: str = Form(None),
                                    email: str = Form(None),
                                    phone: str = Form(None),
                                    page: int = 1,
                                    size: int = 50,
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    if user.user_type not in [1,2]:
        return {"status":0,"msg":"Access denied"}

    students = db.query(User).join(Batch,Batch.id == User.batch_id).join(
            CourseAssign, CourseAssign.user_id == User.id 
        ).filter(Batch.status==1,User.user_type==3,User.status==1,CourseAssign.status==1)
    course_list = []
    
    if course_id:
        students = students.filter(CourseAssign.course_id == course_id)
    if name:
        students = students.filter(User.name.like(f"%{name}%"))
    if email:
        students = students.filter(User.email.ilike(f"%{email}%"))
    if phone:
        students = students.filter(User.phone == phone)
        
    students = students.order_by(User.id.desc())
    totalCount= students.count()

    total_page,offset,limit=get_pagination(totalCount,page,size)
    students=students.limit(limit).offset(offset).all()
    dataList =[]

    for student in students:
        dataList.append({
            "id": student.id,
            "name": student.name.capitalize(),
            "email": student.email,
            "username": student.username,
            "phone": student.phone,
            "address": student.address,
            # "course": student.course.name if student.course else None,
            "batch_id": student.batch_id,
            # "course_id": student.course_id,
            
        })
        
    data=({"page":page,
           "size":size,
           "total_page":total_page,
            "total_count":totalCount,
            "items":dataList})
    
    return {"status":1,"msg":"Success","data":data}






