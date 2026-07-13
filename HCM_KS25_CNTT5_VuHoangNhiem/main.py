from fastapi import FastAPI, status, Depends, HTTPException, Request
from HCM_KS25_CNTT5_VuHoangNhiem.database import Base, engine, get_db
from HCM_KS25_CNTT5_VuHoangNhiem.models import StudentManagerApi
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from typing import Any 
from sqlalchemy.orm import Session
from pydantic import BaseModel


app = FastAPI()

Base.metadata.create_all(bind= engine)

def ApiResponse(
    statusCode: int,
    message: str,
    data: Any,
    error = None
):
    return {
        "statusCode": statusCode,
        "error": error,
        "message": message,
        "data": data,
    }
    
class StudentInput(BaseModel):
    full_name: str
    class_name: str
    email: str
    phone_number: str

class StudentIOutput(BaseModel):
    id: int
    full_name: str
    class_name: str
    email: str
    phone_number: str
    
    model_config = {"from_attributes": True}
    
@app.exception_handler(HTTPException)
async def http_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            statusCode=exc.status_code,
            message=exc.detail,
            data=None,
            error=exc.detail,
        )
    )
    
@app.exception_handler(RequestValidationError)
async def request_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=ApiResponse(
            statusCode=status.HTTP_422_UNPROCESSABLE_CONTENT,
            message="Lỗi dữ liệu nhập vào",
            data=None,
            error=exc.errors(),
        )
    )

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiResponse(
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi dữ liệu ngoại lệ",
            data=None,
            error="Validated error exception",
        )
    )
    
@app.get("/", status_code= status.HTTP_200_OK)
def check_connection():
    return ApiResponse(
        statusCode= status.HTTP_200_OK,
        message="API đang chạy",
        data=None
    )
    
@app.get("/students", status_code=status.HTTP_200_OK)
def list_student(db: Session = Depends(get_db)):
    list_std = db.query(StudentManagerApi).all()
    
    return ApiResponse(
        statusCode= status.HTTP_200_OK,
        message="Danh sách sinh viên",
        data=[StudentIOutput.model_validate(std) for std in list_std]
    )
    
@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
def find_student(student_id: int, db: Session = Depends(get_db)):
    found_std = db.query(StudentManagerApi).filter(StudentManagerApi.id == student_id).first()
    
    if found_std is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sinh viên"
        )
    
    return ApiResponse(
        statusCode= status.HTTP_200_OK,
        message=f"Sinh viên có id là {student_id}",
        data=found_std
    )

@app.post("/students")
def add_student(student: StudentInput, db: Session = Depends(get_db)):
    student = student.model_dump()
    new_std = StudentManagerApi(
        full_name= student["full_name"],
        class_name= student["class_name"],
        email= student["email"],
        phone_number= student["phone_number"]
    )
    
    db.add(new_std)
    db.commit()
    db.refresh(new_std)
    
    return ApiResponse(
        statusCode= status.HTTP_201_CREATED,
        message="Đã thêm sinh viên thành công",
        data=new_std
    )

@app.put("/students/{student_id}")
def update_student_id(student_id: int,student: StudentInput, db: Session = Depends(get_db)):
    update_std = db.query(StudentManagerApi).filter(StudentManagerApi.id == student_id).first()
    
    if update_std is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sinh viên"
        )
    
    update_std.full_name = student.full_name
    update_std.class_name = student.class_name
    update_std.email = student.email
    update_std.phone_number = student.phone_number
    
    db.commit()
    db.refresh(update_std)
    
    return ApiResponse(
        statusCode= status.HTTP_200_OK,
        message="Đã cập nhật sinh viên thành công",
        data=update_std
    )
    
@app.delete("/students/{student_id}")
def delete_student(student_id: int,db: Session = Depends(get_db)):
    delete_std = db.query(StudentManagerApi).filter(StudentManagerApi.id == student_id).first()
    
    if delete_std is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sinh viên"
        )
    
    db.delete(delete_std)
    db.commit()
    
    return ApiResponse(
        statusCode= status.HTTP_200_OK,
        message="Đã xóa sinh viên thành công",
        data=None
    )