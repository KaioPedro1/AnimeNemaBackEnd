from typing import List
from fastapi import FastAPI, Depends, status, APIRouter
from sqlalchemy.orm import Session
from utilidades import utilidades
from database import schemas, database, models

router = APIRouter(
    prefix="/users"
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user.senha = utilidades.hash(user.senha)
    novo_usuario = models.User(**user.dict())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/", response_model=List[schemas.UserOutput])
def get_usuarios( db: Session = Depends(database.get_db)):
    usuarios = db.query(models.User).all()
    return (usuarios)
