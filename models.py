from sqlalchemy import Column, Integer, String
from database import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    user_email = Column(String, index=True)
    age = Column(Integer, index=True)
    recommendations = Column(String, index=True)
    ZIP = Column(Integer, index=True)