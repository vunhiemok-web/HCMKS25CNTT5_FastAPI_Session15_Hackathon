from HCM_KS25_CNTT5_VuHoangNhiem.database import Base, engine
from sqlalchemy import Column, Integer, String

class StudentManagerApi(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(50))
    class_name = Column(String(15))
    email = Column(String(15))
    phone_number = Column(String(15))
    
Base.metadata.create_all(bind= engine)