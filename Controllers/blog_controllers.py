
from fastapi import Depends
from DataBase.connect import ConnectDB
from sqlalchemy.orm import Session
from Schemas.blog_schemas import Blog , UpdateBlog
from Midddlewares.auth_middleware import verifyJWT
from Models.sql_models import BlogModel
from utils.response import CustomResponse
from fastapi import status


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
        data=new_blog
    )


def getAllBlogs(db : Session = Depends(ConnectDB)):
    blogs = db.query(BlogModel).all()
    if not blogs:
        return  CustomResponse.error(
        message='No Blogs Found!',
    )
    return  CustomResponse.success(
        message='Blogs fetched successfully!',
        data=blogs
    )




def getSingleBlogById(id : int , db : Session = Depends(ConnectDB)):

    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
          return  CustomResponse.error(
        message='Blog Not Found !',
    )
    return  CustomResponse.success(
        message='Blog fetched successfully!',
        data=blog
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
                )
        else:
            if(current_blog.createdBy == current_user['id']):
                db.delete(current_blog)
                db.commit()
                return  CustomResponse.success(
                message='Blog deleted successfully!')


def updateBlogById(id : int , update_blog : UpdateBlog,   db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user:
        return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    else:
        current_blog = db.query(BlogModel).filter(BlogModel.id == id).first()
        print('Cureent Blog : ' , current_blog)
        if not current_blog:
             return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
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
                data=current_blog)
            else:
                return CustomResponse.error(
            message=' Not Authenticated ! ',
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    