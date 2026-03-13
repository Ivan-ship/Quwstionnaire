from pydantic import BaseModel, EmailStr

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