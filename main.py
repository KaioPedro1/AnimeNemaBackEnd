from fastapi import FastAPI
from database import database
from database import models
from routers import user, autenticacao, anime, tipoTicket, auditorio,sessoes,poltronas, reservas, slider
from utilidades import configuracao
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(autenticacao.router)
app.include_router(anime.router)
app.include_router(tipoTicket.router)
app.include_router(auditorio.router)
app.include_router(sessoes.router)
app.include_router(poltronas.router)
app.include_router(reservas.router)
app.include_router(slider.router)

@app.get("/")
async def root():
    return{"message": "Funciona, funciona!"}


