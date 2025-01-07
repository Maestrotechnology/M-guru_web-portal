from typing import Generator, Any, Optional
from fastapi.security import OAuth2PasswordBearer
import datetime
from sqlalchemy.orm import Session
from app import models
import random,os,sys
from sqlalchemy import or_
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from datetime import datetime,timedelta
import hashlib
from app.models import ApiTokens,User
from app.models import User
from app.core.config import settings
from fpdf import FPDF

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
            filter( models.User.username == username 
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

def get_username(db: Session,type: int):
    user = db.query(User).filter(User.status==1,User.user_type==type).order_by(User.id.desc()).first()
    if type==2:
        prefix = "MENTOR"
        if not user:
           return "MENTOR101"
        else:
            digit = int(user.username[6:])+1
            if digit<10:
                digit = "0"+str(digit) 
            return prefix+str(digit)
    elif type == 3:
        prefix = "MGURU"
        if not user:
           return "MGURU101"
        else:
            digit = int(user.username[5:])+1
            if digit<10:
                digit = "0"+str(digit) 
            return prefix+str(digit)
import math
def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of Earth in meters
    R = 6371000  
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in meters
    distance = R * c
    return distance

def add_header(pdf, logo_path="asset/logo.png"):
    # Outer border
    pdf.set_draw_color(0, 0, 0)
    pdf.rect(5, 5, 200, 287)

    # Green and yellow triangle background
    pdf.set_fill_color(0, 102, 0)  # Dark green
    pdf.polygon([(5, 5), (50, 5), (5, 25)], 'F')
    pdf.set_fill_color(255, 204, 0)  # Yellow
    pdf.polygon([(140, 5), (205, 5), (205, 25)], 'F')

    # Logo
    pdf.image(logo_path, 80, 10, 50)

    # M-GURU Text
    # pdf.set_font("Helvetica", "B", 28)
    # pdf.set_text_color(0, 102, 204)  # Blue
    # pdf.set_xy(60, 10)
    # pdf.cell(0, 10, "M", align="L")
    # pdf.set_text_color(0, 0, 0)  # Black
    # pdf.cell(0, 10, "Guru", align="L")

    # Student's Mark Sheet Text
    # pdf.set_font("Times", "B", 16)
    # pdf.set_text_color(0, 0, 128)  # Navy Blue
    # pdf.set_xy(60, 20)
    # pdf.cell(0, 10, title, align="C")

    # Date
    # pdf.set_font("Times", "B", 12)
    # pdf.set_text_color(0, 0, 0)
    # if is_month == 1:
    #     pdf.set_xy(147, 7.5)
    #     pdf.cell(0, 10, f"Date : {from_date.strftime('%d-%m-%Y')} - {to_date.strftime('%d-%m-%Y')}", align="L")
    # else:
    #     pdf.set_xy(165, 7.5)
    #     pdf.cell(0, 10, f"Date : {to_date.strftime('%d-%m-%Y')}", align="L")

    # Divider line below the header
    pdf.line(5, 27, 205, 27)

def pdf_file_storage(file_name: str, f_name: str):
    base_dir = settings.BASE_UPLOAD_FOLDER + "/upload_files/"
    # dt = str(int(datetime.now().timestamp()))
    dt = 1
    
    try:
        os.makedirs(base_dir, mode=0o777, exist_ok=True)
    except OSError as e:
        sys.exit(f"Can't create {base_dir}: {e}")
    
    output_dir = base_dir
    files_name = f_name.split(".")
    save_full_path = f"{output_dir}{files_name[0]}_{dt}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.output(save_full_path)
    file_exe = f"upload_files/{files_name[0]}_{dt}.pdf"
    
    return save_full_path, file_exe


class CustomPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.1)
        self.line(10, self.get_y() - 3, 200, self.get_y() - 3)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def calculate_row_height(pdf, col_widths, data_row, line_height):
    heights = []
    for col_width, cell_data in zip(col_widths, data_row):
        lines = pdf.multi_cell(col_width, line_height, cell_data, border=0, align="L", split_only=True)
        heights.append(len(lines) * line_height)
    return max(heights)