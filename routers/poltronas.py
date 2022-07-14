from typing import List, Optional
from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import schemas, database, models

router = APIRouter(
    prefix="/poltronas"
)

#terminar usando join

@router.get("/",response_model= List[schemas.PoltronaOutput])
def get_all_poltronas(db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0):
    poltronas = db.query(models.Poltronas).limit(limit).offset(skip).all()
    return (poltronas)

@router.get("/{id}",response_model= List[schemas.PoltronaOutput])
def get_all_poltronas(id: int, db: Session = Depends(database.get_db)):
    poltronas = db.query(models.Poltronas).filter(models.Poltronas.sessoes_id == id).all()
    return (poltronas)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.PoltronaOutput)
def inserir_poltrona(poltrona_input: schemas.PoltronasBase, db: Session = Depends(database.get_db)):
    nova_poltrona = models.Poltronas(**poltrona_input.dict())
    try:
        db.add(nova_poltrona)
        db.commit()
        db.refresh(nova_poltrona)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Não foi possivel inserir a poltrona, poltrona ocupada.")
    return nova_poltrona

"""
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_anime(id: int, db: Session = Depends(database.get_db)):
    anime_query = db.query(models.Animes).filter(models.Animes.id == id)
    if not anime_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar o anime Id({id}) no banco de dados")
    anime_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.AnimeOutput)
def atualizar_anime(id: int, updated_post: schemas.AnimeBase, db: Session = Depends(database.get_db)):
    anime_query = db.query(models.Animes).filter(models.Animes.id == id)
    anm = anime_query.first()
    if not anm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar o anime Id({id}) no banco de dados")
    anime_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return (anm)
"""