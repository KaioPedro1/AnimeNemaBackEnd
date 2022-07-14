from typing import List, Optional
from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import schemas, database, models

router = APIRouter(
    prefix="/animes"
)


@router.get("/", response_model=List[schemas.AnimeOutput])
def get_all_animes(db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    animes = db.query(models.Animes).filter(models.Animes.nome.contains(search)).limit(limit).offset(skip).all()
    return (animes)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.AnimeOutput)
def inserir_anime(anime_input: schemas.AnimeBase, db: Session = Depends(database.get_db)):
    novo_anime = models.Animes(**anime_input.dict())
    db.add(novo_anime)
    db.commit()
    db.refresh(novo_anime)
    return novo_anime

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
