from typing import List, Optional
from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import schemas, database, models

router = APIRouter(
    prefix="/slider",
    tags=['sliderHomepage']
)


@router.get("/", response_model=List[schemas.SliderHomepageOutput])
def get_all_animes_carrousel(db: Session = Depends(database.get_db)):
    animes = db.query(models.Slider_homepage.id, models.Slider_homepage.posicao_slide, models.Animes.nome,
                      models.Animes.cover_img_url, models.Animes.descricao_en, models.Slider_homepage.anime_id)\
        .outerjoin(models.Animes, models.Slider_homepage.anime_id == models.Animes.id)\
        .all()
    return (animes)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.SliderHomepageInput)
def inserir_anime_carrousel(anime_input: schemas.SliderHomepageInput, db: Session = Depends(database.get_db)):
    novo_anime = models.Slider_homepage(**anime_input.dict())
    try:
        db.add(novo_anime)
        db.commit()
        db.refresh(novo_anime)
    except: raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f"Posicao já ocupada no banco de dados")
    return novo_anime

@router.put("/{id}", response_model=schemas.SliderHomepageInput)
def atualizar_carrousel(id: int, updated_post: schemas.SliderHomepageInput, db: Session = Depends(database.get_db)):
    try:
        anime_query = db.query(models.Slider_homepage).filter(models.Slider_homepage.id == id)
        anm = anime_query.first()
        if not anm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar o anime Id({id}) no banco de dados")
        anime_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()
    except: raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Posicao já ocupada no banco de dados")
    return (anm)
