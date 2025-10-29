from pydantic import BaseModel ,Field ,EmailStr
from typing import List , Optional , Annotated
from datetime import date


class CommentSchema(BaseModel):
    id : Annotated[Optional[int],Field(description='Unique id of the comment',examples=[1,2,3],default=None)]

    Blog_id : Annotated[Optional[int],Field(description='Id of the blog on which comment is present',examples=[1],default=None)]

    content  : Annotated[str,Field(...,description='content  of the comment',examples=['Content of the blog.'])]
    Date : Annotated[
        Optional[date],
        Field(description="Date of the comment", examples=["2025-10-25"], default_factory=date.today)
    ]

    commentedBy : Annotated[Optional[int],Field(description='ID of the user who ceated the comment',default=None,examples=[1])]

    model_config = {
        "from_attributes": True
    }




class UpdateCommentSchema(BaseModel):
    content  : Annotated[Optional[str],Field(description='content  of the comment',examples=['Content of the blog.'])]


    model_config = {
        "from_attributes": True
    }