from database import Base
from sqlalchemy import Column,String,Integer,Text,ForeignKey,Enum
from enum import Enum as PyEnum

class AccountTypeEnum(PyEnum):
    CURRENT='Current'
    SAVINGS='Savings'
    SALARY='Salary'
    FIXED_DEPOSIT='Fixed deposit'
    RECURRING_DEPOSIT='Recurring deposit'
    NRI='NRI'

class Account(Base):
    __abstract__ = True

    id = Column(Integer,primary_key=True,index=True)
    branchName = Column(String(100))
    accountNumber = Column(String(18),nullable=False)
    ifscCode = Column(String(11),nullable=False)
    bankAddress = Column(Text)
    accountType = Column(Enum(AccountTypeEnum),nullable=False)
    
class UserTypeEnum(PyEnum):
    ADMIN='Admin'
    USER='User'

class UserAccount(Account):
    __tablename__="UserAccount"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    mobileNumber = Column(String(16))
    address = Column(Text)
    password = Column(String(255))
    userType=Column(Enum(UserTypeEnum),nullable=False)
