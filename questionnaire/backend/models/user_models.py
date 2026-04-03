from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, DateTime
from routers.database import Base
from datetime import datetime

class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    
#Вход пользователя
class LoginUser(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool | None = False
    
    
class Confirm(BaseModel):
    email: EmailStr
    activation_code: str

class ResetRequest(BaseModel):
    email: EmailStr
    new_password: str

class ResetConfirm(BaseModel):
    email: EmailStr
    activation_code: str

class User(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_ad = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PendingUser(Base):
    __tablename__ = "pending_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    activation_code = Column(String)
    created_ad = Column(DateTime, default=datetime.utcnow)

class ResetPassword(Base):
    __tablename__ = "reset_passwords"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    new_password = Column(String)
    code = Column(String)
    created_ad = Column(DateTime, default=datetime.utcnow)