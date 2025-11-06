from pydantic import BaseModel

class UserRead(BaseModel):
    uuid: str
    username: str

    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
