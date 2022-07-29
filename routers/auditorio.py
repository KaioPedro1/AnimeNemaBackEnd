from typing import List, Optional
from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import schemas, database, models

router = APIRouter(
    prefix="/auditorio",
    tags = ['Auditorio']
)


@router.get("/", response_model=List[schemas.AuditorioOutput])
def get_all_auditorios(db: Session = Depends(database.get_db), limit: int = 100, skip: int = 0, search: Optional[str]=""):
    auditorios = db.query(models.Auditorio).filter(models.Auditorio.nome.contains(search)).limit(limit).offset(skip).all()
    return (auditorios)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.AuditorioOutput)
def inserir_auditorio(auditorio_input: schemas.AuditorioBase, db: Session = Depends(database.get_db)):
    novo_auditorio = models.Auditorio(**auditorio_input.dict())
    db.add(novo_auditorio)
    db.commit()
    db.refresh(novo_auditorio)
    return novo_auditorio

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_tipo_ticket(id: int, db: Session = Depends(database.get_db)):
    auditorio_query = db.query(models.Auditorio).filter(models.Auditorio.id == id)
    if not auditorio_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar o auditório({id}) no banco de dados")
    auditorio_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.AuditorioOutput)
def atualizar_anime(id: int, auditorio_atualizado: schemas.AuditorioBase, db: Session = Depends(database.get_db)):
    auditorio_query = db.query(models.Auditorio).filter(models.Auditorio.id == id)
    auditorio = auditorio_query.first()
    if not auditorio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar o auditório Id({id}) no banco de dados")
    auditorio_query.update(auditorio_atualizado.dict(), synchronize_session=False)
    db.commit()
    return (auditorio)
