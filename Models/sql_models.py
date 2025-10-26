from DataBase.connect import Base
from sqlalchemy import Column , Integer , Text , String ,func ,Date,ForeignKey
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer,index=True,autoincrement=True,primary_key=True,unique=True)
    fullName = Column(String)
    username = Column(String,unique=True)
    password = Column(String)
    email = Column(String,unique=True)

    MyLikes = relationship('LikeModel',back_populates='LikedBy')
    MyComments = relationship('CommentModel',back_populates='CommentedBy')
    MyBlogs = relationship('BlogModel',back_populates='createdBy')

    class Config:
        orm_mode = True



class BlogModel(Base):

    __tablename__ = 'blogs'
    
    id = Column(Integer,index=True,autoincrement=True,primary_key=True,unique=True)
    title = Column(String)
    content = Column(Text)
    createdAt = Column(Date,default=func.current_timestamp())
    createdBy = Column(Integer,ForeignKey('users.id'),nullable=True)

    owner = relationship('UserModel',back_populates='MyBlogs')

    class Config :
        orm_mode = True



class LikeModel(Base):
    __tabelname__ = 'likes'
    id =  Column(Integer,unique=True,autoincrement=True,index=True)
    Blog_id = Column(Integer,ForeignKey('blogs.id'),nullable=True)
    createdAt = Column(Date,default=func.current_timestamp())
    LikedBy = Column(Integer,ForeignKey('users.id'),nullable=True)

    owner = relationship('UserModel',back_populates='MyLikes')

    class Config :
        orm_mode = True



class CommentsModel(Base):
    __tablename__ = 'comments'
    id =  Column(Integer,unique=True,autoincrement=True,index=True)
    content = Column(String)
    Blog_id = Column(Integer,ForeignKey('blogs.id'),nullable=True)
    createdAt = Column(Date,default=func.current_timestamp())
    CommentedBy =Column(Integer,ForeignKey('users.id'),nullable=True)

    owner = relationship('UserModel',back_populates='MyComments')


    class Config :
        orm_mode = True

