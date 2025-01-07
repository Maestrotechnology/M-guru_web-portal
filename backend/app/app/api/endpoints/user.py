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
from api.deps import *
from fpdf import FPDF
from app.api.endpoints.email_templetes import get_email_templete
router = APIRouter()

@router.post("/create_user")
async def createUser(db:Session=Depends(get_db),
                     token:str = Form(...),
                     name:str = Form(...),
                     user_type:int=Form(...,description=("1->admin,2>Trainer, 3>Student")),
                     email:EmailStr=Form(...),
                     phone:str=Form(...),
                     address:str=Form(None),
                     password:str=Form(...),
                     course_id:str=Form(None,description='if multiple 1,2,3,4,5'),
                     batch_id:int=Form(None)
                     
):
    
    user = get_user_token(db,token=token)
    
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}

    if user_type in [2,3]:
        if not course_id:
            return {"status":0,"msg":"Course required"}
    # if user_type == 3 and batch_id is None:
    #     return {"status":0,"msg":"Batch required for student"}
    checkUser = db.query(User).filter(User.status==1)
    print(batch_id)
    if user_type !=3 or (user_type ==3 and batch_id == None):
        print(2222)
        if checkUser.filter(User.email == email).first():
            return {"status":0,"msg":"Given Email is already exist"}
        if checkUser.filter(User.phone==phone).first():
            return {"status":0,"msg":"Given Phone Number is already exist"}
    elif user.user_type ==3 and batch_id:
        print(1111)
        if checkUser.filter(User.email == email,User.batch_id==batch_id).first():
            uuuuu = checkUser.filter(User.email == email,User.batch_id==batch_id).first()
            print(uuuuu.id)
            return {"status":0,"msg":"Given Email is already exist"}
        if checkUser.filter(User.phone==phone,User.batch_id==batch_id).first():
            return {"status":0,"msg":"Given Phone Number is already exist"}
    
    hashPassword = get_password_hash(password)
    addUser =  User(
                    name=name,
                    username = get_username(db,user_type),
                    user_type=user_type,
                    email=email,
                    phone=phone,
                    password=hashPassword,
                    create_at = datetime.now(settings.tz_IN),
                    status =1,
                    address=address,
                    batch_id=batch_id,
                    # course_id=course_id
                    )
    db.add(addUser)
    db.commit()
    if course_id:
        course_ids = course_id.split(',')
        for course in course_ids:
            add_course = CourseAssign(
                user_id = addUser.id,
                course_id = course,
                created_by = user.id,
                created_at = datetime.now(settings.tz_IN),
                status = 1
            )
            db.add(add_course)
            db.commit()

    await send_mail(receiver_email=addUser.email,message=get_email_templete(addUser,None,6,username= addUser.username,password=password),subject="M-GURU Login detail")
    return {
        "status" : 1,
        "msg":"User created successfully"
    }

@router.post("/update_user")
async def updateUser(
                     db:Session=Depends(get_db),
                     token:str=Form(...),
                     name:str = Form(...),
                     userId:int=Form(...),
                     email:EmailStr=Form(...),
                     phone:str=Form(...),
                     address:str=Form(None),
                     course_id:str=Form(None,description='if multiple 1,2,3'),
                     ):
    
    user  = get_user_token(db,token=token)

    if not user:
        return {"status":0,"msg":"Account details not found"}
    
    checkUser = db.query(User).filter(User.status==1)

    getUser = checkUser.filter(User.id == userId,User.status==1).first()

    if not getUser:
        return {"status":0,"msg":"Given user id  not found"}
        
    # if getUser.user_type == 3 and not course_id:
    #     return {"status":0, "msg": "course is required"}

    # if username:
    #     if checkUser.filter(User.username == username,User.id!=userId).first():
    #         return {"status":0,"msg":"Given userName is already exist"}
    #     getUser.username = username
    if email:
        if checkUser.filter(User.email == email,User.id!=userId).first():
            return {"status":0,"msg":"Given Email is already exist"}
    if phone:
        if checkUser.filter(User.phone==phone,User.id!=userId).first():
            return {"status":0,"msg":"Given Phone Number is already exist"}
    getUser.email = email
    getUser.phone =  phone
    getUser.name=name
    getUser.address=address
    getUser.update_at=datetime.now()
    db.commit()
    if course_id:
        # Convert course_id to a list of integers (split the comma-separated string)
        course_ids = [int(course) for course in course_id.split(",")]

        # Get all course assignments for the user
        assigned_courses = db.query(CourseAssign).filter(
            CourseAssign.user_id == userId
        ).all()

        # Create a set of course IDs the user should have access to
        # courses_to_assign = set(course_ids)

        # Handle each assigned course
        for course_assignment in assigned_courses:
            if course_assignment.course_id not in course_ids:
                # If the course is not in the new list, update its status to -1
                course_assignment.status = -1
                course_assignment.updated_at = datetime.now(settings.tz_IN)
                db.commit()
            else:
                # If the course is in the new list, ensure it's active
                if course_assignment.status != 1:
                    course_assignment.status = 1  # Reactivate course
                    course_assignment.updated_at = datetime.now(settings.tz_IN)
                    db.commit()

                # Remove it from the courses_to_assign set (it's already handled)
                course_ids.remove(course_assignment.course_id)

        # Add new courses that are not already assigned
        for new_course_id in course_ids:
            new_course_assign = CourseAssign(
                user_id=userId,
                course_id=new_course_id,
                created_by=user.id,
                created_at=datetime.now(settings.tz_IN),
                updated_at=datetime.now(settings.tz_IN),
                status=1
            )
            db.add(new_course_assign)
            db.commit()
    return {"status":1, "msg":"User details updated successfully."}




@router.post("/list_user")
async def list_user(
                   db:Session=Depends(deps.get_db),
                   token:str=Form(...),
                   userType:int=Form(...,description="1-> admin 2>Trainer, 3>Student"),
                   user_id: int = Form(None),
                   course_id: int = Form(None),
                   batch_id: int = Form(None),
                   email: str = Form(None),
                   username:str=Form(None),
                   phoneNumber:int=Form(None),
                   page:int=1,
                   size:int=50,
):
    user=deps.get_user_token(db=db,token=token)
    if not user:
        return({'status' :-1,'msg' :'Sorry! your login session expired. please login again.'})
    
    if userType not in[1,2,3]:
        return {"status":0, "msg":"Invalid user type"}
    
    if batch_id:
        get_batch = db.query(Batch).filter(Batch.id==batch_id,Batch.status==1).first()
        if not get_batch:
            return {"status":0, "msg":"Invalid batch"}
    
    get_user = db.query(User).filter(User.status!=-1,User.user_type == userType)

    if batch_id:
        get_user = get_user.filter(User.batch_id==batch_id)
    if course_id:
        get_user = get_user.join(
            CourseAssign, CourseAssign.user_id == User.id).filter(CourseAssign.course_id == course_id)
    if user_id:
        get_user = get_user.filter(User.id == user_id)
    if email:
        get_user = get_user.filter(User.email == email)
    if username:
        get_user = get_user.filter(User.username.ilike(f"%{username}%"))
    if phoneNumber:
        get_user = get_user.filter(User.phone == phoneNumber)

    get_user = get_user.order_by(User.id.desc())
    totalCount= get_user.count()
    total_page,offset,limit=get_pagination(totalCount,page,size)
    get_user=get_user.limit(limit).offset(offset).all()
    dataList =[]    
    
    for data in get_user:
        course_data = []
        get_course = db.query(Course).join(CourseAssign,Course.id==CourseAssign.course_id).filter(CourseAssign.user_id==data.id,CourseAssign.status==1).all()
        if get_course:
            for course in get_course:
                course_data.append({
                    "Course_Id":course.id,
                    "Course_name":course.name
                })
        dataList.append({
            "batch_id":batch_id,
            "id":data.id,
            "name":data.name.capitalize(),
            "username":data.username,
            "email":data.email,
            "user_type":data.user_type,
            "address":data.address,
            # "course_name":  data.course.name if data.course else None,
            # "course_id": data.course_id,
            "phone": data.phone,
            "course":course_data,
            "status":data.status
        })
    data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":dataList})
    return {"status":1,"msg":"Success","data":data}
   
@router.post("/delete_user")
async def deleteUser(db:Session=Depends(get_db),
                     token:str=Form(...),
                     userId:int=Form(...)
):
    
    user  = get_user_token(db,token=token)

    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type == 1 or user.user_type == 2:
        getUser = db.query(User).filter(User.id == userId,User.status == 1).first()

        if not getUser :
            return {"status":0, "msg":"Given user id details not found"}
        
        getUser.status = -1
        db.commit()
        return {"status":1, "msg":"User details successfully deleted"}
    else:
        return {"status":0,"msg":"You are not authenticate to delete the user"}
                
@router.post("/profile")
async def profile(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
):
    user  = get_user_token(db,token=token)

    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_course_details = db.query(Course).join(CourseAssign,CourseAssign.course_id==Course.id
                        ).filter(CourseAssign.status==1,CourseAssign.user_id==user.id,Course.status==1).all()
    course_data = []
    for course in get_course_details:
        course_data.append({
            "CourseId":course.id,
            "CourseName":course.name
        })
    return {
        "status":1,
        "msg":"Success",
        "data":{
        "user_id": user.id,
        "name": user.name,
        "username": user.username,
        "phone": user.phone,
        "address": user.address,
        "course": course_data,
        "batch": user.batch.name if user.batch_id else None,
        "user_type": user.user_type,
        "email": user.email,
        "batch_start_date": user.batch.start_date.strftime("%Y-%m-%d") if user.batch_id else None,}
    }
    
@router.post("/active_inactive_user")
async def activeInactiveUser(*,db : Session = Depends(get_db),token:str=Form(...),
                              user_id : int = Form(...),status : int = Form(...,description="1-> active 2-> inactive")):
    user  = get_user_token(db,token=token)
    if status not in [1,2]:
        return {"status":0,"msg":"Invalid status"}
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    if user.user_type != 1:
        return {"status":0,"msg":"Access denied"}
    get_user = db.query(User).filter(User.status != -1,User.id ==user_id).first()
    if not get_user:
        return {"status":0,"msg":"User not found."}
    get_user.status = status
    db.commit()
    msg = "User Inactivated successfully." if status ==2 else "User activated successfully"
    return {"status":1,"msg":msg}

# "created_at":data.project_detail.created_at.strftime("%d-%m-%Y") if data.student_project_id and data.project_detail.created_at else "-",

@router.post("/view_mark_sheet")
async def viewMarkSheet(*,db : Session = Depends(get_db),token:str=Form(...),
                              student_id : int = Form(...),):
    user  = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_student = db.query(User).filter(User.status!=-1,User.id==student_id,User.user_type==3).first()
    if not get_student:
        return {"status":0,"msg":"User Not found"}
    get_assigned_course = db.query(CourseAssign).filter(CourseAssign.status==1,CourseAssign.user_id==student_id).all()
    course_data = []
    for course in get_assigned_course:
        course_data.append(course.course.name)
    assigned_exams = db.query(AssignExam).filter(AssignExam.student_id == student_id,AssignExam.status==1).all()

    if not assigned_exams:
        return {"status": 0, "msg": "No exams found for this student."}

    data_list = []
    
    for assigned_exam in assigned_exams:
        # Get the exam details
        exam = db.query(Exam).filter(Exam.id == assigned_exam.exam_id).first()
        
        if not exam:
            continue  # Skip if exam doesn't exist (shouldn't happen, but to be safe)

        # Get assigned questions for this exam
        assigned_questions = db.query(AssignedQuestion).filter(AssignedQuestion.assign_exam_id == assigned_exam.id).all()
        # Calculate the total marks for the exam
        total_marks = sum(questions.question.mark for questions in assigned_questions)
        # Get the student's answers for the exam
        student_exam_details = db.query(StudentExamDetail).filter(
            StudentExamDetail.assign_exam_id == assigned_exam.id,
            StudentExamDetail.student_id == student_id
        ).all()
        
        # Calculate the student's score
        student_score = sum(detail.mark for detail in student_exam_details)
        
        # Get the name of the person who assigned the exam
        assigned_by_user = db.query(User).filter(User.id == assigned_exam.assigned_by).first()
        
        # Prepare the exam summary data
        exam_data = {
            "assigned_by": assigned_exam.assigner.name if assigned_exam.assigned_by and assigned_exam.assigner.name else None,
            "exam_name": exam.name if exam else "Unknown Exam",
            "assigned_name": assigned_by_user.name if assigned_by_user else "Unknown Assigner",
            "total_marks": total_marks,
            "student_score": student_score,
            "exam_id": assigned_exam.id,
            "attended_date": student_exam_details[0].created_at if student_exam_details and student_exam_details[0] else None,
            "exam_date" : assigned_exam.created_at.strftime("%d-%m-%Y")
        }
        data_list.append(exam_data)
    task_data = []
    get_student_score = db.query(Score).join(Task,Task.id == Score.task_id).filter(Score.student_id==student_id,Score.status==1,Task.status == 1).all()
    for data in get_student_score:
        task_data.append({
            "id":data.id,
            "mark":data.mark,
            "task_id":data.task_id,
            "task_name":data.task.name,
            "student_id":data.student_id,
            "student_name":data.student.name.capitalize(),
            "mark_giver_id": data.teacher_id,
            "mark_giver_name":data.teacher.name,
            "created_at":data.project_detail.created_at.strftime("%d-%m-%Y") if data.student_project_id and data.project_detail.created_at else "-",
        })
    
    pdf = CustomPDF()
    pdf.add_page()
    logo_path = "asset/logo.png"
    add_header(pdf,logo_path)

    pdf.set_font("Times", "B", 16)
    pdf.set_text_color(0, 0, 128)  # Navy Blue
    pdf.set_xy(10, 30)
    pdf.cell(0, 10, "Student Mark Sheet", align="C")

    pdf.ln(5)
    pdf.set_font("Times", "", 12)
    pdf.set_fill_color(200, 220, 255)

    # Table Headers
    pdf.ln(5)  # Line break before the student details section
    pdf.set_font("Times", "B", 12)
    pdf.set_text_color(0, 0, 0)
    # Student Name
    pdf.cell(40, 10, "Student Name", border=1, align="L")
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 10, get_student.name, border=1, align="L")
    pdf.ln()

    # Student Email
    pdf.set_font("Times", "B", 12)
    pdf.cell(40, 10, "Email", border=1, align="L")
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 10, get_student.email, border=1, align="L")
    pdf.ln()

    # Batch Information
    pdf.set_font("Times", "B", 12)
    pdf.cell(40, 10, "Batch (From - To)", border=1, align="L")
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 10, f"{get_student.batch.name} ({get_student.batch.start_date.strftime('%d-%m-%Y')} - {get_student.batch.end_date.strftime('%d-%m-%Y ')})", border=1, align="L")
    pdf.ln()

    # Courses Assigned to Student
    pdf.set_font("Times", "B", 12)
    pdf.cell(40, 10, "Courses", border=1, align="L")
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 10, ", ".join(course_data), border=1, align="L")
    pdf.ln(10)

    # Task Scores Table
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 10, "Task Scores", ln=True, align="C")
    pdf.set_font("Times", "", 12)

    # Task Table Headers
    headers = ["S.No", "Task Name", "Uploaded Date", "Evaluator", "Mark"]
    col_widths = [12, 70, 40, 50, 20]

    # Create Header Row
    pdf.set_font("Times", "B", 12)
    for header, col_width in zip(headers, col_widths):
        pdf.cell(col_width, 10, header, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Times", "", 12)   
    # Loop through tasks and display data
    serial_no = 1
    for task in task_data:
        if pdf.get_y() > 265:
            pdf.add_page()
        row_data = [
            str(serial_no),
            task["task_name"],
            task["created_at"],
            task["mark_giver_name"],
            str(task["mark"]),
        ]
        
        # Calculate the height of "Task Name" without rendering (based on text length)
        task_name = row_data[1] 
        task_name_width = col_widths[1]  
        
        text_width = pdf.get_string_width(task_name)  
        lines_needed = int(text_width / (task_name_width - 2)) + 1
        task_name_height = lines_needed * 6 
        
        y_start = pdf.get_y()  
        max_height = task_name_height
        
        # Render "S.No" cell
        x_start = pdf.get_x()
        pdf.cell(col_widths[0], max_height, row_data[0], border=1, align="C")
        pdf.set_xy(x_start + col_widths[0], y_start) 

        # Render "Task Name" cell
        x_start = pdf.get_x()  
        pdf.multi_cell(task_name_width, 6, row_data[1], border=1, align="C")
        pdf.set_xy(x_start + task_name_width, y_start) 

        # Render "Uploaded At" cell
        x_start = pdf.get_x()  
        pdf.cell(col_widths[2], max_height, row_data[2], border=1, align="C")
        pdf.set_xy(x_start + col_widths[2], y_start)  

        # Render "Evaluator" cell
        x_start = pdf.get_x()  
        pdf.cell(col_widths[3], max_height, row_data[3], border=1, align="C")
        pdf.set_xy(x_start + col_widths[3], y_start) 

        # Render "Mark" cell
        x_start = pdf.get_x()  
        pdf.cell(col_widths[4], max_height, row_data[4], border=1, align="C")
        pdf.set_xy(x_start + col_widths[4], y_start)

        pdf.set_y(y_start + max_height)
        serial_no += 1

    # Exam Results Table
    if pdf.get_y() > 265:
            pdf.add_page()
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 10, "Exam Results", ln=True, align="C")

    # Exam Table Headers
    headers = ["S.No", "Exam Date", "Exam Name", "Assigned By", "Total Marks", "Student Score"]
    col_widths = [12, 40, 50, 40, 25, 25]

    # Create Header Row
    for header, col_width in zip(headers, col_widths):
        pdf.cell(col_width, 10, header, border=1, align="C", fill=True)
    pdf.ln()
    pdf.set_font("Times", "", 12)
    if pdf.get_y() > 265:
            pdf.add_page()

    # Loop through exam data
    serial_no = 1
    for exam_data in data_list:
        if pdf.get_y() > 265:
            pdf.add_page()
        row_data = [
            str(serial_no),
            exam_data["exam_date"],
            exam_data["exam_name"],
            exam_data["assigned_name"],
            str(exam_data["total_marks"]),
            str(exam_data["student_score"])
        ]

        # Calculate the height of "Exam Name" without rendering (based on text length)
        exam_name = row_data[2]  # Exam Name
        exam_name_width = col_widths[2]  # Column width for "Exam Name"
        
        text_width = pdf.get_string_width(exam_name)  # Get the width of the exam name text
        lines_needed = int(text_width / (exam_name_width - 2)) + 1  # Calculate how many lines are needed for the text
        exam_name_height = lines_needed * 6  # Each line is ~6 units tall

        # Calculate the max height for the row (based on Exam Name's height)
        max_height = exam_name_height
        
        # Save current Y position
        y_start = pdf.get_y()

        # Render "S.No" cell
        x_start = pdf.get_x()  # Save current X position
        pdf.cell(col_widths[0], max_height, row_data[0], border=1, align="C")
        pdf.set_xy(x_start + col_widths[0], y_start)  # Align cursor for next cell

        # Render "Exam Date" cell
        x_start = pdf.get_x()
        pdf.cell(col_widths[1], max_height, row_data[1], border=1, align="C")
        pdf.set_xy(x_start + col_widths[1], y_start)  # Align cursor for next cell

        # Render "Exam Name" cell
        x_start = pdf.get_x()  # Save current X position
        pdf.multi_cell(exam_name_width, 6, row_data[2], border=1, align="C")
        pdf.set_xy(x_start + exam_name_width, y_start)  # Align cursor for next cell

        # Render "Assigned By" cell
        x_start = pdf.get_x()
        pdf.cell(col_widths[3], max_height, row_data[3], border=1, align="C")
        pdf.set_xy(x_start + col_widths[3], y_start)  # Align cursor for next cell

        # Render "Total Marks" cell
        x_start = pdf.get_x()
        pdf.cell(col_widths[4], max_height, row_data[4], border=1, align="C")
        pdf.set_xy(x_start + col_widths[4], y_start)  # Align cursor for next cell

        # Render "Student Score" cell
        x_start = pdf.get_x()
        pdf.cell(col_widths[5], max_height, row_data[5], border=1, align="C")
        pdf.set_xy(x_start + col_widths[5], y_start)  # Align cursor for next cell

        # Move to the next row, based on the calculated max height
        pdf.ln(max_height)
        serial_no += 1




    # Save the PDF to the file system
    student_name = get_student.name.replace(" ", "_")
    filename = f"{student_name}_Mark_Sheet.pdf"
    save_path, file_path = pdf_file_storage("report", filename)
    pdf.output(save_path)

    return {"status":1,"msg":"success","file_url": f"{settings.BASEURL}/{file_path}"}



# @router.post("/view_mark_sheet")
# async def viewMarkSheet(*,db : Session = Depends(get_db),token:str=Form(...),
#                               student_id : int = Form(...),):
#     user  = get_user_token(db,token=token)
#     if not user:
#         return {"status":0,"msg":"Your login session expires.Please login again."}
#     get_student = db.query(User).filter(User.status!=-1,User.id==student_id,User.user_type==3).first()
#     if not get_student:
#         return {"status":0,"msg":"User Not found"}
#     get_assigned_course = db.query(CourseAssign).filter(CourseAssign.status==1,CourseAssign.user_id==student_id).all()
#     course_data = []
#     for course in get_assigned_course:
#         course_data.append(course.course.name)
#     assigned_exams = db.query(AssignExam).filter(AssignExam.student_id == student_id,AssignExam.status==1).all()

#     if not assigned_exams:
#         return {"status": 0, "msg": "No exams found for this student."}

#     data_list = []
    
#     for assigned_exam in assigned_exams:
#         # Get the exam details
#         exam = db.query(Exam).filter(Exam.id == assigned_exam.exam_id).first()
        
#         if not exam:
#             continue  # Skip if exam doesn't exist (shouldn't happen, but to be safe)

#         # Get assigned questions for this exam
#         assigned_questions = db.query(AssignedQuestion).filter(AssignedQuestion.assign_exam_id == assigned_exam.id).all()
#         # Calculate the total marks for the exam
#         total_marks = sum(questions.question.mark for questions in assigned_questions)
#         # Get the student's answers for the exam
#         student_exam_details = db.query(StudentExamDetail).filter(
#             StudentExamDetail.assign_exam_id == assigned_exam.id,
#             StudentExamDetail.student_id == student_id
#         ).all()
        
#         # Calculate the student's score
#         student_score = sum(detail.mark for detail in student_exam_details)
        
#         # Get the name of the person who assigned the exam
#         assigned_by_user = db.query(User).filter(User.id == assigned_exam.assigned_by).first()
        
#         # Prepare the exam summary data
#         exam_data = {
#             "assigned_by": assigned_exam.assigner.name if assigned_exam.assigned_by and assigned_exam.assigner.name else None,
#             "exam_name": exam.name if exam else "Unknown Exam",
#             "assigned_name": assigned_by_user.name if assigned_by_user else "Unknown Assigner",
#             "total_marks": total_marks,
#             "student_score": student_score,
#             "exam_id": assigned_exam.id,
#             "attended_date": student_exam_details[0].created_at if student_exam_details and student_exam_details[0] else None,
#             "exam_date" : assigned_exam.created_at.strftime("%d-%m-%Y %H:%m")
#         }
#         data_list.append(exam_data)
#     task_data = []
#     get_student_score = db.query(Score).join(Task,Task.id == Score.task_id).filter(Score.student_id==student_id,Score.status==1,Task.status == 1).all()
#     for data in get_student_score:
#         task_data.append({
#             "id":data.id,
#             "mark":data.mark,
#             "task_id":data.task_id,
#             "task_name":data.task.name,
#             "student_id":data.student_id,
#             "student_name":data.student.name.capitalize(),
#             "mark_giver_id": data.teacher_id,
#             "mark_giver_name":data.teacher.name,
#             "created_at":data.project_detail.created_at.strftime("%d-%m-%Y") if data.student_project_id and data.project_detail.created_at else "-",
#         })
    
#     pdf = CustomPDF()
#     pdf.add_page()
#     logo_path = "asset/logo.png"
#     add_header(pdf,logo_path)

#     pdf.set_font("Times", "B", 16)
#     pdf.set_text_color(0, 0, 128)  # Navy Blue
#     pdf.set_xy(10, 30)
#     pdf.cell(0, 10, "Student Mark Sheet", align="C")

#     pdf.ln(5)
#     pdf.set_font("Times", "", 12)
#     pdf.set_fill_color(200, 220, 255)

#     # Table Headers
#     pdf.ln(5)  # Line break before the student details section
#     pdf.set_font("Times", "", 12)
#     pdf.set_text_color(0, 0, 0)
#     # Student Name
#     pdf.cell(40, 10, "Student Name", border=1, align="L", fill=True)
#     pdf.cell(0, 10, get_student.name, border=1, align="L")
#     pdf.ln()

#     # Student Email
#     pdf.cell(40, 10, "Email", border=1, align="L", fill=True)
#     pdf.cell(0, 10, get_student.email, border=1, align="L")
#     pdf.ln()

#     # Batch Information
#     pdf.cell(40, 10, "Batch (From - To)", border=1, align="L", fill=True)
#     pdf.cell(0, 10, f"{get_student.batch.name} ({get_student.batch.start_date.strftime('%d-%m-%Y')} - {get_student.batch.end_date.strftime('%d-%m-%Y ')})", border=1, align="L")
#     pdf.ln()

#     # Courses Assigned to Student
#     pdf.cell(40, 10, "Courses", border=1, align="L", fill=True)
#     pdf.cell(0, 10, ", ".join(course_data), border=1, align="L")
#     pdf.ln(10)

#     pdf.cell(0, 10, "Task Scores", ln=True, align="C")
#     pdf.set_font("Times", "", 12)

#     # Task Table Headers
#     pdf.cell(12, 10, "S.No", border=1, align="C", fill=True)
#     pdf.cell(70, 10, "Task Name", border=1, align="C", fill=True)
#     pdf.cell(40, 10, "Uploaded At", border=1, align="C", fill=True)
#     pdf.cell(50, 10, "Evaluator", border=1, align="C", fill=True)
#     pdf.cell(20, 10, "Mark", border=1, align="C", fill=True)
#     pdf.ln()

#     # Loop through tasks and display data
#     serial_no = 1
#     for task in task_data:
#         pdf.cell(12, 10, str(serial_no), border=1, align="C")
#         pdf.cell(70, 10, task["task_name"], border=1, align="C")
#         pdf.cell(40, 10, task["created_at"], border=1, align="C")
#         pdf.cell(50, 10, task["mark_giver_name"], border=1, align="C")
#         pdf.cell(20, 10, str(task["mark"]), border=1, align="C")
#         pdf.ln()
#         serial_no += 1

#     # Exam Results Table
#     pdf.cell(0, 10, "Exam Results", ln=True, align="C")
#     # pdf.ln(5)
#     pdf.set_font("Times", "", 12)

#     # Exam table headers
#     pdf.cell(12, 10, "S.No", border=1, align="C", fill=True)
#     pdf.cell(40, 10, "Exam Date", border=1, align="C", fill=True)
#     pdf.cell(50, 10, "Exam Name", border=1, align="C", fill=True)
#     pdf.cell(40, 10, "Assigned By", border=1, align="C", fill=True)
#     pdf.cell(25, 10, "Total Marks", border=1, align="C", fill=True)
#     pdf.cell(25, 10, "Student Score", border=1, align="C", fill=True)
#     pdf.ln()

#     # Loop through exams and display data
#     serial_no = 1
#     for exam_data in data_list:
#         pdf.cell(12, 10, str(serial_no) , border=1, align="C")
#         pdf.cell(40, 10, exam_data["exam_date"], border=1, align="C")
#         pdf.cell(50, 10, exam_data["exam_name"], border=1, align="C")
#         pdf.cell(40, 10, exam_data["assigned_name"], border=1, align="C")
#         pdf.cell(25, 10, str(exam_data["total_marks"]), border=1, align="C")
#         pdf.cell(25, 10, str(exam_data["student_score"]), border=1, align="C")
#         pdf.ln()
#         serial_no +=1

#     # Save the PDF to the file system
#     student_name = get_student.name.replace(" ", "_")
#     filename = f"{student_name}_Mark_Sheet.pdf"
#     save_path, file_path = pdf_file_storage("report", filename)
#     pdf.output(save_path)

#     return f"{settings.BASEURL}/{file_path}"