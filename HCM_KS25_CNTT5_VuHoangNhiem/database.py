from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE = "mysql+pymysql://root2:123456@localhost:3306/student_db"

engine = create_engine(DATABASE)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit= False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()