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