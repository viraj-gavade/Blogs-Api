from pydantic import BaseModel ,Field ,EmailStr
from typing import List , Optional , Annotated
from datetime import date


class Blog(BaseModel):
    id : Annotated[Optional[int],Field(description='Unique id of the blog',examples=[1,2,3],default=None)]

    title : Annotated[str,Field(...,description='Title of the blogs',examples=['Machine Learning'])]

    content  : Annotated[str,Field(...,description='content  of the blogs',examples=['Content of the blog.'])]

    Date : Annotated[
        Optional[date],
        Field(description="Date of the Blog", examples=["2025-10-25"], default_factory=date.today)
    ]

    createdBy : Annotated[int,Field(description='ID of the user who ceated the blog',default=None)]

    LikedBy : Annotated[Optional[List[int]],Field(description='Id of the  users liked blogs',default=None)]

    CommentedBy : Annotated[Optional[List[int]],Field(description='Id of the  users commented blogs',default=None)]





class UpdateBlog(BaseModel):
    title : Annotated[Optional[str],Field(description='Title of the blogs',examples=['Machine Learning'],default=None)]

    content  : Annotated[Optional[str],Field(description='content  of the blogs',examples=['Content of the blog.'],default=None)]



