from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.classes import Class

router = APIRouter()

@router.get("/")
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(Class).all()
    return classes
