from typing import Generator, Any, Optional
from datetime import datetime,timedelta
import random
from sqlalchemy.orm import Session
from sqlalchemy import * 
from app.models import *
from sqlalchemy import *
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.models import ApiTokens,User

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()