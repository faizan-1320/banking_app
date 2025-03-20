from database import Base
from sqlalchemy import Column,String,Integer,Text,ForeignKey,Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class AccountTypeEnum(PyEnum):
    CURRENT='Current'
    SAVINGS='Savings'
    SALARY='Salary'
    FIXED_DEPOSIT='Fixed deposit'
    RECURRING_DEPOSIT='Recurring deposit'
    NRI='NRI'

class Account(Base):
    __tablename__="accounts"

    id = Column(Integer,primary_key=True,index=True)
    branchName = Column(String(100))
    accountNumber = Column(String(18),unique=True,nullable=True)
    ifscCode = Column(String(11),nullable=True)
    bankAddress = Column(Text)
    accountType = Column(Enum(AccountTypeEnum),nullable=True)

    userAccounts = relationship('UserAccount', back_populates='account', cascade="all, delete")
    
class UserTypeEnum(PyEnum):
    ADMIN='Admin'
    USER='User'

class User(Base):
    __tablename__="users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    mobileNumber = Column(String(16))
    address = Column(Text)
    password = Column(String(255))
    userType=Column(Enum(UserTypeEnum),nullable=False,default=UserTypeEnum.USER)

    userAccounts = relationship('UserAccount', back_populates='user', cascade="all, delete")

class UserAccount(Base):
    __tablename__="userAccounts"

    id = Column(Integer,primary_key=True,index=True)
    accountId = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)

    account = relationship('Account', back_populates='userAccounts')
    user = relationship('User', back_populates='userAccounts')