from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, BLOB

Base = declarative_base()

db = SQLAlchemy() 
 
class Users(db.Model):
    __tablename__ = 'users'
 
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    email = Column(String(45))
    password = Column(String(20))

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
     
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
 
    def __repr__(self):
        return "<users(%s, %s, %s, %s )>" % (
            self.name, self.login, self.email, self.password)

    
    def get_id(self):
        return str(self.id)
    
    
    def serialize(self):
        return {
            "name":self.name,
            "email":self.email
        }
    
    
    

class Files(db.Model):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    id_user= Column(Integer)
    filename= Column(String(60))
    content = Column(BLOB)
    date = Column(Date)

    def __init__(self, id_user, filename, content, date):
        self.id_user = id_user
        self.filename = filename
        self.content = content
        self.date =date

    def __repr__(self):
        return "<files(%s,%s,%s)>" % (self.id_user, self.filename, self.date)
        
    def serialize(self):
        return {"Nome do arquivo": str(self.filename), "Data": str(self.date)}