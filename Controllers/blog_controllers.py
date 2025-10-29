
from fastapi import Depends
from DataBase.connect import ConnectDB
from sqlalchemy.orm import Session
from Schemas.blog_schemas import Blog , UpdateBlog
from Midddlewares.auth_middleware import verifyJWT
from Models.sql_models import BlogModel
from utils.response import CustomResponse
from fastapi import status
from Models.sql_models import LikeModel , CommentsModel
from fastapi.encoders import jsonable_encoder



def createBlog(blog : Blog , db : Session = Depends(ConnectDB), current_user = Depends(verifyJWT) ):
    print('Current User :  ' , current_user)
    userId = current_user['id']

    if not userId:
        return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    else:
        new_blog = BlogModel(
            title = blog.title,
            content = blog.content,
            createdBy = userId
        )

        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return CustomResponse.success(
        message='Blog Created successfully!',
        data= jsonable_encoder(new_blog),
        status_code=status.HTTP_201_CREATED
    )


def getAllBlogs(db : Session = Depends(ConnectDB)):
    blogs = db.query(BlogModel).all()
    if not blogs:
        return  CustomResponse.error(
        message='No Blogs Found!',
        status_code=status.HTTP_404_NOT_FOUND
    )
    return  CustomResponse.success(
        message='Blogs fetched successfully!',
        data=jsonable_encoder(blogs)
    )




def getSingleBlogById(id : int , db : Session = Depends(ConnectDB)):

    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    blog_comments = db.query(CommentsModel).filter(CommentsModel.Blog_id == id).all()
    blog_likes = db.query(LikeModel).filter(LikeModel.Blog_id == id).all()
    if not blog:
        return CustomResponse.error(
            message=' Blog Not Found ! ',
            status_code= status.HTTP_404_NOT_FOUND
        )
    data = {
        'Blog ':  blog,
        'Comments ' : blog_comments,
        'Likes ' : blog_likes
    }
    return  CustomResponse.success(
        message='Blog fetched successfully!',
        data=jsonable_encoder(data)
    )


def deleteBlogById(id : int , db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user:
        return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    else:
        current_blog = db.query(BlogModel).filter(BlogModel.id == id).first()
        if not current_blog:
               return  CustomResponse.error(
                message='Blog Not Found !',
                status_code=status.HTTP_404_NOT_FOUND
                )
        else:
            if(current_blog.createdBy == current_user['id']):
                db.delete(current_blog)
                db.commit()
                return  CustomResponse.success(
                message='Blog deleted successfully!')
            else:
                return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )



def updateBlogById(id : int , update_blog : UpdateBlog,   db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user:
        return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    else:
        current_blog = db.query(BlogModel).filter(BlogModel.id == id).first()
        if not current_blog:
             return CustomResponse.error(
            message=' Blog Not Found ! ',
            status_code= status.HTTP_404_NOT_FOUND
        )
        else:
            if(current_blog.createdBy == current_user['id']):
                update_data = update_blog.model_dump(exclude_unset=True)

                for key , value in update_data.items():
                    setattr(current_blog,key,value)
                db.commit()
                db.refresh(current_blog)
                return  CustomResponse.success(
                message='Blog updated successfully!',
                data=jsonable_encoder(current_blog))
            else:
                return CustomResponse.error(
            message=' Not Authenticated to Update the Blog ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    