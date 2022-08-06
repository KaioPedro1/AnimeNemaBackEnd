from typing import List, Optional
from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import schemas, database, models

router = APIRouter(
    prefix="/sessoes",
    tags = ['Sessoes']
)



@router.get("/", response_model=List[schemas.SessoesOutput])
def get_all_sessoes(db: Session = Depends(database.get_db), limit: int = 100, skip: int = 0):
    sessoes = db.query(models.Sessoes).limit(limit).offset(skip).all()
    return (sessoes)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.SessoesOutput)
def inserir_sessao(sessoes_input: schemas.SessoesBase, db: Session = Depends(database.get_db)):
    nova_sessao = models.Sessoes(**sessoes_input.dict())
    try:
        db.add(nova_sessao)
        db.commit()
        db.refresh(nova_sessao)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Não foi possivel inserir a sessao no banco de dados, sala ocupada neste horario")
    return nova_sessao


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_sessao(id: int, db: Session = Depends(database.get_db)):
    sessao_query = db.query(models.Sessoes).filter(models.Sessoes.id == id)
    if not sessao_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar a sessao({id}) no banco de dados")
    sessao_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.SessoesOutput)
def atualizar_sessao(id: int, sessoes_atualizado: schemas.SessoesBase, db: Session = Depends(database.get_db)):
    sessoes_query = db.query(models.Sessoes).filter(models.Sessoes.id == id)
    sessoes= sessoes_query.first()
    if not sessoes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar o auditório Id({id}) no banco de dados")
    try:
        sessoes_query.update(sessoes_atualizado.dict(), synchronize_session=False)
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Não foi possivel alterar a sala, sala ocupada neste horario")
    return (sessoes)