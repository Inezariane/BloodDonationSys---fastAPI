from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Define the base class for SQLAlchemy
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    def __str__(self):
        return self.username

# BloodGroup model
class BloodGroup(Base):
    __tablename__ = 'blood_groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(5))

    def __str__(self):
        return self.name

# RequestBlood model
class RequestBlood(Base):
    __tablename__ = 'requests_blood'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    city = Column(String(300), default="")
    address = Column(String(500), default="")
    blood_group_id = Column(Integer, ForeignKey('blood_groups.id'))
    date = Column(String(100), default="")

    blood_group = relationship('BloodGroup', back_populates='requests')

    def __str__(self):
        return self.name

# Donor model
class Donor(Base):
    __tablename__ = 'donors'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  
    first_name = Column(String)  
    last_name = Column(String)  
    email = Column(String, unique=True)  
    password = Column(String)  
    date_of_birth = Column(String(100))
    phone = Column(String(10))
    city = Column(String(100))
    address = Column(String(500), default="")
    blood_group_id = Column(Integer, ForeignKey('blood_groups.id'))
    gender = Column(String(10))
    ready_to_donate = Column(Boolean, default=True)
    blood_group = relationship('BloodGroup', back_populates='donors')


    def __str__(self):
        return str(self.blood_group)

# Define the back_populates relationships in the BloodGroup model
BloodGroup.donors = relationship('Donor', back_populates='blood_group')
BloodGroup.requests = relationship('RequestBlood', back_populates='blood_group')
