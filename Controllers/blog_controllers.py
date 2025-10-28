
from fastapi.requests import Request
from fastapi import Depends
from DataBase.connect import ConnectDB
from sqlalchemy.orm import Session
from Schemas.blog_schemas import Blog , UpdateBlog
from Midddlewares.auth_middleware import verifyJWT
from Models.sql_models import BlogModel



def createBlog(blog : Blog , db : Session = Depends(ConnectDB), current_user = Depends(verifyJWT) ):
    print('Current User :  ' , current_user)
    userId = current_user['id']

    if not userId:
        return 'Login to create a Blog'
    else:
        new_blog = BlogModel(
            title = blog.title,
            content = blog.content,
            createdBy = userId
        )

        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return {'message:':"Blog Created Successfully",'data': new_blog}


def getAllBlogs(db : Session = Depends(ConnectDB)):
    blogs = db.query(BlogModel).all()
    if not blogs:
        return 'NO Blogs found!'
    return blogs




def getSingleBlogById(id : int , db : Session = Depends(ConnectDB)):

    blog = db.query(BlogModel).filter(BlogModel.id == id).first()
    if not blog:
        return f'No blog with the id {id}'
    return blog


def deleteBlogById(id : int , db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user:
        return 'Not Authenticated'
    else:
        current_blog = db.query(BlogModel).filter(BlogModel.id == id).first()
        print('Cureent Blog : ' , current_blog)
        if not current_blog:
            return f'No blog found with the id {id}'
        else:
            if(current_blog.createdBy == current_user['id']):
                db.delete(current_blog)
                db.commit()
                return 'Blog Deleted sucessfully!'

def updateBlogById(id : int , update_blog : UpdateBlog,   db : Session = Depends(ConnectDB),current_user = Depends(verifyJWT)):
    if not current_user:
        return 'Not Authenticated'
    else:
        current_blog = db.query(BlogModel).filter(BlogModel.id == id).first()
        print('Cureent Blog : ' , current_blog)
        if not current_blog:
            return f'No blog found with the id {id}'
        else:
            if(current_blog.createdBy == current_user['id']):
                update_data = update_blog.model_dump(exclude_unset=True)

                for key , value in update_data.items():
                    setattr(current_blog,key,value)
                db.commit()
                db.refresh(current_blog)
                return current_blog
    