from typing import List
from fastapi import FastAPI, Depends, status, APIRouter,HTTPException,Response
from sqlalchemy.orm import Session
from utilidades import utilidades
from database import schemas, database, models

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        user.senha = utilidades.hash(user.senha)
        novo_usuario = models.User(**user.dict())
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Usuario já está cadastrado")
    return novo_usuario

@router.get("/", response_model=List[schemas.UserOutput])
def get_usuarios( db: Session = Depends(database.get_db)):
    usuarios = db.query(models.User).all()
    return (usuarios)

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_usuario(id: int, db: Session = Depends(database.get_db)):
    delete_user_query = db.query(models.User).filter(models.User.id == id)
    if not delete_user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar o Id({id}) no banco de dados")
    delete_user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

