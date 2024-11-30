import datetime
from sqlalchemy.orm import Session
import random
from app.core.config import settings
from datetime import datetime, timedelta, date, time
import string
from app.core.config import settings
from app.models import *
from sqlalchemy import or_, and_
import sys
import math
import os
import shutil
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import smtplib
from email_validator import validate_email, EmailNotValidError
import tracemalloc
from email.mime.text import MIMEText 

tracemalloc.start()

def get_timer(data):
    time1 = data.created_at
    time2 = datetime.now()

    time_difference = (time2 - time1).total_seconds() / 60
    # hours = time_diff.seconds // 3600
    # minutes = (time_diff.seconds % 3600) // 60
    return (f"{int(time_difference)}")


# async def send_mail(receiver_email, message):  # Demo
#     sender_email = "maestronithishraj@gmail.com"
#     receiver_email = receiver_email
#     password = "ycjanameheveewtb"

#     msg = message
#     print(msg)
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.ehlo()
#     server.starttls()
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, msg)
#     server.quit()

#     return True
async def send_mail(receiver_email,subject,message):  # Demo
    sender_email = "maestronithishraj@gmail.com"
    receiver_email = receiver_email
    password = "ycjanameheveewtb"
    
    msg = MIMEText(message,"html")
 
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Application status"
 
    # msg = str(message)
    print(msg)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.ehlo()
    # server.starttls()
    # server.login(sender_email, password)
    # server.sendmail(sender_email, receiver_email, msg)
    # server.quit()
 
    return True


def file_storage(file_name, f_name):

    base_dir = settings.BASE_UPLOAD_FOLDER+"/m-guru"

    dt = str(int(datetime.utcnow().timestamp()))

    try:
        os.makedirs(base_dir, mode=0o777, exist_ok=True)
    except OSError as e:
        sys.exit("Can't create {dir}: {err}".format(
            dir=base_dir, err=e))

    output_dir = base_dir + "/"

    filename = file_name.filename
    # Split file name and extension
    

    txt = filename[::-1]
    splitted = txt.split(".", 1)
    txt1 = splitted[0][::-1]
    txt2 = splitted[1][::-1]

    files_name = f_name.split(".")
    
    save_full_path = f'{output_dir}{files_name[0]}{dt}.{txt1}'
    print()
    file_exe = f"m-guru/{files_name[0]}{dt}.{txt1}"
    # print(file_exe)
    with open(save_full_path, "wb") as buffer:
        shutil.copyfileobj(file_name.file, buffer)

    return save_full_path, file_exe


def store_file(file):

    base_dir = settings.BASE_UPLOAD_FOLDER+"/upload_files/"

    dt = str(int(datetime.utcnow().timestamp()))

    try:
        os.makedirs(base_dir, mode=0o777, exist_ok=True)
    except OSError as e:
        sys.exit("Can't create {dir}: {err}".format(
            dir=base_dir, err=e))

    filename = file.filename

    file_properties = filename.split(".")

    file_extension = file_properties[-1]

    file_properties.pop()
    file_splitted_name = file_properties[0]

    write_path = f"{base_dir}{file_splitted_name}{dt}.{file_extension}"
    db_path = f"/upload_files/{file_splitted_name}{dt}.{file_extension}"

    with open(write_path, "wb") as new_file:
        shutil.copyfileobj(file.file, new_file)

    return db_path


def pagination(row_count=0, page=1, size=10):
    current_page_no = page if page >= 1 else 1

    total_pages = math.ceil(row_count / size)

    if current_page_no > total_pages:
        current_page_no = total_pages

    limit = current_page_no * size
    offset = limit - size

    if limit > row_count:
        limit = offset + (row_count % size)

    limit = limit - offset

    if offset < 0:
        offset = 0

    return [limit, offset]


def get_pagination(row_count=0, current_page_no=1, default_page_size=10):
    current_page_no = current_page_no if current_page_no >= 1 else 1

    total_pages = math.ceil(row_count / default_page_size)

    if current_page_no > total_pages:
        current_page_no = total_pages

    limit = current_page_no * default_page_size
    offset = limit - default_page_size

    if limit > row_count:
        limit = offset + (row_count % default_page_size)

    limit = limit - offset

    if offset < 0:
        offset = 0

    return [total_pages, offset, limit]


def paginate(page, size, data, total):
    reply = {"items": data, "total": total, "page": page, "size": size}
    return reply


def paginate_for_file_count(page, size, data, total, file_count):
    reply = {"items": data, "total": total, "page": page,
             "file_count": file_count, "size": size}
    return reply


# async def send_emails(from_mail, to_mail, subject, message):
#     conf = ConnectionConfig(
#         MAIL_USERNAME="emailtomaestro@gmail.com",  # "testmaestromail@gmail.com",
#         MAIL_PASSWORD="prdwskswxgqlsjqa",  # testmaestro@123",
#         MAIL_FROM="emailtomaestro@gmail.com",  # from_mail,
#         MAIL_PORT=587,
#         MAIL_SERVER="smtp.gmail.com",  # "smtp.gmail.com",
#         MAIL_FROM_NAME="MConnect",  # from_mail,
#         MAIL_TLS=True,
#         MAIL_SSL=False,
#         VALIDATE_CERTS=True,
#         USE_CREDENTIALS=True
#     )
#     message = MessageSchema(
#         subject=subject,
#         recipients=[to_mail],
#         body=message,
#     )

#     fm = FastMail(conf)
#     await fm.send_message(message)
#     return True


def common_date(date, without_time=None):

    datetime = date.strftime("%d-%m-%Y %I:%M:%S")

    if without_time == 1:
        datetime = date.strftime("%d-%m-%Y")
    if without_time == 2:
        datetime = date.strftime("%I:%M:%S")

    return datetime


def check(email):
    try:
        v = validate_email(email)
        email = v["email"]
        return True
    except EmailNotValidError as e:
        return False

# def convert_tz(time_data, from_zone: str, to_zone: str) -> datetime:

#     # METHOD 1: Hardcode zones:
#     # from_zone = tz.gettz('UTC')
#     # to_zone = tz.gettz('Asia/Kolkata')

#     from_zn = from_zone.split(' (') if from_zone else None
#     to_zn = to_zone.split(' (') if from_zone else None

#     from_zone = tz.gettz(from_zn[0])
#     to_zone = tz.gettz(to_zn[0])

#     # METHOD 2: Auto-detect zones:
#     # from_zone = tz.tzutc()
#     # to_zone = tz.tzlocal()

#     # utc1 = datetime.utcnow()
#     from_time = time_data
#     if type(time_data) == str:
#         try:
#             from_time = datetime.strptime(time_data, '%Y-%m-%d %H:%M:%S')
#         except:
#             from_time = datetime.strptime(time_data, '%Y-%m-%dT%H:%M:%S')
#     from_time_zone = from_time.replace(tzinfo=from_zone, microsecond=0)

#     # Convert time zone
#     to_time = from_time_zone.astimezone(to_zone)

#     return to_time.replace(tzinfo=None)


def getTimeDifferenceDate(start,end):
    timeDifference = end - start
    minutesDifference = timeDifference.total_seconds() / 60
    return int(minutesDifference) 