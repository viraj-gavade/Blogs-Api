from pydantic import BaseModel ,Field ,EmailStr
from typing import List , Optional , Annotated



class User(BaseModel):
    id : Annotated[int,Field(description='Unique id of the user',examples=[1,2,3])]

    fullName : Annotated[str,Field(...,description='Full Name of the user',examples=['Viraj Gavade'])]

    email : Annotated[EmailStr,Field(...,description='Email of the user',examples=['vrajgavade17@gmail.com'])]

    password : Annotated[str,Field(...,description='Password  of the user',examples=['admin123'],pattern=r"^[A-Za-z0-9]{8,}$",max_length=24)]

    username : Annotated[str,Field(...,description='username  of the user',examples=['viraj_gavade'],pattern=r'^[a-zA-Z0-9_]+$',max_length=16)]

    MyLikes : Annotated[Optional[List[int]],Field(description='Id of the  user liked blogs',default=None)]

    MyComments : Annotated[Optional[List[int]],Field(description='Id of the  user commented blogs',default=None)]

    MyBlogs : Annotated[Optional[List[int]],Field(description='Id of the all blogs posted by user',default=None)]






class SignupUser(BaseModel):
    id : Annotated[Optional[int],Field(description='Unique id of the user',examples=[1,2,3],default=None)]

    fullName : Annotated[str,Field(...,description='Full Name of the user',examples=['Viraj Gavade'])]

    email : Annotated[EmailStr,Field(...,description='Email of the user',examples=['vrajgavade17@gmail.com'])]

    password : Annotated[str,Field(...,description='Password  of the user',examples=['admin123'],pattern=r"^[A-Za-z0-9]{8,}$",max_length=24)]

    username : Annotated[str,Field(...,description='username  of the user',examples=['viraj_gavade'],pattern=r'^[a-zA-Z0-9_]+$',max_length=16)]

    model_config = {"from_attributes": True}

class SignInUser(BaseModel):
    
    username : Annotated[str,Field(...,description='username  of the user',examples=['viraj_gavade'],pattern=r'^[a-zA-Z0-9_]+$',max_length=16)]

    password : Annotated[str,Field(...,description='Password  of the user',examples=['admin123'],pattern=r"^[A-Za-z0-9]{8,}$",max_length=24)]
    model_config = {"from_attributes": True}


class UpdateUser(BaseModel):

    fullName : Annotated[Optional[str],Field(description='Full Name of the user',examples=['Viraj Gavade'],default=None)]

    email : Annotated[Optional[EmailStr],Field(description='Email of the user',examples=['vrajgavade17@gmail.com'],default=None)]

    username : Annotated[Optional[str],Field(description='username  of the user',examples=['viraj_gavade'],pattern=r'^[a-zA-Z0-9_]+$',max_length=16,default=None)]

    model_config = {"from_attributes": True}

class UserPublic(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}