from fastapi import APIRouter
from app.api.v1.endpoints import auth, students, classes, student_data, analysis, curriculum

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])
api_router.include_router(student_data.router, prefix="/student-data", tags=["student-data"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(curriculum.router, prefix="/curriculum", tags=["curriculum"])
