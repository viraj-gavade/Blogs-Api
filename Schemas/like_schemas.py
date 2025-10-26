from pydantic import BaseModel ,Field ,EmailStr
from typing import List , Optional , Annotated
from datetime import date


class Like(BaseModel):
    id : Annotated[int,Field(...,description='Unique id of the blog',examples=[1,2,3])]

    Blog_id : Annotated[int,Field(...,description='Id of the blog on which like is present',examples=[1])]

    Date : Annotated[
        Optional[date],
        Field(description="Date of the like", examples=["2025-10-25"], default_factory=date.today)
    ]

    LikedBy : Annotated[Optional[int],Field(description='ID of the user who ceated the blog',default=None,examples=[1])]