from pydantic import BaseModel, EmailStr


class UserValidateSchema(BaseModel):
    name: str
    email: EmailStr
    age: int