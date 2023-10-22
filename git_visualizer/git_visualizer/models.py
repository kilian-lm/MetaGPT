## models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    projects = relationship('Project', order_by='Project.id', back_populates='user')

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='projects')

    def __init__(self, id: int, name: str, user_id: int, user: User):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.user = user

    versions = relationship('Version', order_by='Version.id', back_populates='project')

class Version(Base):
    __tablename__ = 'versions'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    timestamp = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='versions')

    def __init__(self, id: int, content: str, timestamp: datetime, project_id: int, project: Project):
        self.id = id
        self.content = content
        self.timestamp = timestamp
        self.project_id = project_id
        self.project = project
