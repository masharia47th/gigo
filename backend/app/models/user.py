
from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from enum import Enum as PyEnum

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Role(str, PyEnum):
    tenant = "tenant"
    care_taker = "care_taker"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def hash_password(cls, password: str):
        return pwd_context.hash(password)
