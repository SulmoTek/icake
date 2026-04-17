from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from database import SessionFactory
from service import UserService
from domain.vo import (
    UserLoginRequest,
    UserRegisterRequest, UserInfoResponse,
    UserPasswordResetRequest, UserUpdateRequest
)
from utils import ApiResponse

app = FastAPI(title="小蛋糕 API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

file_router = APIRouter(prefix="/files", tags=["文件上传"])
user_router = APIRouter(prefix="/user", tags=["用户模块"])

@file_router.post("/upload")
def upload(files: list[UploadFile] = File(...)):
    os.makedirs("upload/files", exist_ok=True)
    filenames = []
    for file in files:
        filename = file.filename or "unknown"
        save_path = f"upload/files/{filename}"
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        filenames.append(filename)
    return ApiResponse.success(data={"filenames": filenames})

@user_router.post("/login")
def login(req: UserLoginRequest):
    with SessionFactory() as db:
        token, user = UserService.login(db, req)
        return ApiResponse.success(data={
            "token": token,
            "user": UserInfoResponse.model_validate(user)
        })

@user_router.post("/register")
def register(req: UserRegisterRequest):
    with SessionFactory() as db:
        user = UserService.register(db, req)
        return ApiResponse.success(data=UserInfoResponse.model_validate(user).model_dump())

@user_router.post("/reset-password")
def reset_password(req: UserPasswordResetRequest):
    with SessionFactory() as db:
        UserService.reset_password(db, req)
        return ApiResponse.success(msg="密码重置成功")

@user_router.post("/update")
def update_info(req: UserUpdateRequest, user_id: int = 1):
    with SessionFactory() as db:
        user = UserService.update_info(db, user_id, req)
        return ApiResponse.success(data=UserInfoResponse.model_validate(user))

app.include_router(file_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
