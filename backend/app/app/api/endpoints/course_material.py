from fastapi import APIRouter,Depends,Form,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import *
from app.core.security import settings
from datetime import datetime
from app.utils import *

router = APIRouter()

@router.post("/create_course_material")
async def createCourseMaterial(
                                db: Session = Depends(get_db),
                                token: str = Form(...),
                                course_id: int = Form(...),
                                description: str = Form(None),
                                name: str = Form(),
                                list_material: list[UploadFile] = File(None)
):
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    if user.user_type==3:
        return {"status":0,"msg":"Access denied"}
    course_material = CourseMaterial(
        name = name,
        description = description,
        status = 1,
        created_at = datetime.now(settings.tz_IN),
        updated_at = datetime.now(settings.tz_IN),
        created_by_user_id = user.id,
        course_id = course_id
    )
    db.add(course_material)
    db.commit()
    if list_material:
        for material in list_material:
            file_path, file_url = file_storage(material, material.filename)
            course_media = CourseMedia(
                file_url = file_url,
                status = 1,
                course_material_id = course_material.id,
                created_at = datetime.now(settings.tz_IN),
                updated_at = datetime.now(settings.tz_IN)
            )
            db.add(course_media)
            db.commit()
    return {"status":1,"msg":"Course material successfully created"}

@router.post("/list_course_materials")
async def listCourseMaterials(
                                db: Session = Depends(get_db),
                                token: str = Form(...),
                                course_material_id: int = Form(None),
                                course_id: int = Form(...),
                                name: str = Form(None),
                                page:int=1,
                                size:int=50,
):
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}

    get_course_materials = db.query(CourseMaterial).filter(
                            CourseMaterial.course_id == course_id, CourseMaterial.status ==1
                            )
    if course_material_id:
        get_course_materials = get_course_materials.filter(CourseMaterial.id == course_material_id)

    if user.user_type == 3:
        
        get_course_materials = get_course_materials.filter(CourseMaterial.batch_id==user.batch_id)

    if name:
        get_course_materials = get_course_materials.filter(CourseMaterial.name.like(f"%{name}%"))

    get_course_materials = get_course_materials.order_by(CourseMaterial.id)
    totalCount= get_course_materials.count()
    total_page,offset,limit=get_pagination(totalCount,page,size)
    get_course_materials=get_course_materials.limit(limit).offset(offset).all()

    data_list = []
    for data in get_course_materials:
        data_list.append({
            "id": data.id,
            "name": data.name.capitalize(),
            "description": data.description,
            "course_id": data.course_id,
            "course_name": data.course.name,
            "created_by": data.created_by.name,
            "batch_id": data.batch_id,
            "batch": data.batch.name if data.batch else None,
            "created_at": data.created_at.strftime("%d-%m-%Y"),
            "updated_at": data.updated_at.strftime("%d-%m-%Y"),
            "documents": [{"id": doc.id, "url": f"{settings.BASEURL}/{doc.file_url}"} for doc in data.documents] if data.documents else None

        })           
    data=({"page":page,
           "size":size,
           "total_page":total_page,
           "total_count":totalCount,
           "items":data_list})
            
    return ({"status":1,"msg":"Success.","data":data})

@router.post("/update_course_material")
async def updateCourseMaterials(
                                db: Session = Depends(get_db),
                                token: str = Form(...),
                                course_material_id: int = Form(...),
                                course_id: int = Form(...),
                                description: str = Form(None),
                                name: str = Form(),
                                list_material: list[UploadFile] = File(None),
                                batch_id: int = Form(None),
                                # deleted_material_ids: str = Form(None)
):
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_course_material = db.query(CourseMaterial).filter(CourseMaterial.id==course_material_id,CourseMaterial.status==1).first()
    if not get_course_material:
        return {"status":0,"msg":"Material not found"}
    
    if batch_id:
        get_course_material.batch_id = batch_id

    if user.user_type not in [1,2]:
        return {"status":0,"msg":"Access denied"}
    # if deleted_material_ids:
    #     deleted_material_ids = deleted_material_ids.split(",")
        
    #     materials_to_update = db.query(CourseMedia).filter(CourseMedia.id.in_(deleted_material_ids)).all()
        
    #     for material in materials_to_update:
    #         material.status = -1
        
    #     db.commit()

    get_course_material.course_id = course_id
    get_course_material.description = description
    get_course_material.name = name
    get_course_material.updated_at = datetime.now(settings.tz_IN)
    db.commit()
    if list_material:

        existing_documents = db.query(CourseMedia).filter(
            CourseMedia.course_material_id == get_course_material.id
        ).all()
        for doc in existing_documents:
            doc.status=-1
            db.add(doc)
            db.commit()

        for material in list_material:
            file_path, file_url = file_storage(material, material.filename)
            course_media = CourseMedia(
                file_url=file_url,
                status=1,
                course_material_id=get_course_material.id,
                created_at=datetime.now(settings.tz_IN),
                updated_at=datetime.now(settings.tz_IN)
            )
            db.add(course_media)
            db.commit()
    return {"status":1,"msg":"Successfully Updated"}

@router.post("/delete_course_material")
async def deleteCourseMaterial(
                                db: Session = Depends(get_db),
                                token: str = Form(...),
                                course_material_id: int = Form(...),
):
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    course_material = db.query(CourseMaterial).filter(CourseMaterial.id == course_material_id,CourseMaterial.status==1).first()

    if not course_material:
        return {"status":0,"msg":"Material not found"}
    
    course_material.status = -1
    db.add(course_material)
    db.commit()
    return {"status":1,"msg":"Material deleted successfully"}

@router.post("/delete_course_media")
async def deleteCourseMedia(
                            db: Session = Depends(get_db),
                            token: str = Form(...),
                            course_media_id: int = Form(...)
):
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type not in [1,2]:
        return {"status":0,"msg":"Access denied"}
    
    course_media = db.query(CourseMedia).filter(CourseMedia.id == course_media_id).first()
    if not course_media:
        return {'status':0,'msg':'Course media not found'}
    course_media.status = -1
    db.commit()
    return {"status":1,"msg":"Successfully deleted"}
