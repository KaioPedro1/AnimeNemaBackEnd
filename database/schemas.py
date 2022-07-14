from typing import Optional
from pydantic import BaseModel, EmailStr, AnyUrl
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    senha: str


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    acces_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class AnimeBase(BaseModel):
    nome: str
    score_anilist: Optional[int] = None
    origem: Optional[str] = None
    descricao_en: str
    cover_img_url: AnyUrl
    banner_cover_img_url: Optional[AnyUrl] = None

class AnimeOutput(AnimeBase):
    id: int
    created_at = datetime

    class Config:
        orm_mode = True

class TicketTypeBase(BaseModel):
    tipo: str
    valor: float

class TicketTypeOutput(TicketTypeBase):
    id: int
    class Config:
        orm_mode = True

class AuditorioBase(BaseModel):
    nome: str
    capacidade: int

class AuditorioOutput(AuditorioBase):
    id: int
    class Config:
        orm_mode = True

class SessoesBase(BaseModel):
    anime_id: int
    auditorio_id: int
    horario: datetime

class SessoesOutput(SessoesBase):
    id:int
    anime: AnimeOutput
    auditorio: AuditorioOutput
    class Config:
        orm_mode = True

#terminar poltronas usando JOIN
class AnimePoltronaOutput(BaseModel):
    id: int
    nome: str
    class Config:
        orm_mode = True

class SessoesPoltronaOutput(BaseModel):
    id: int
    anime: AnimePoltronaOutput
    auditorio: AuditorioOutput
    class Config:
        orm_mode = True

class PoltronasBase(BaseModel):
    numero_poltrona: int
    sessoes_id: int

class PoltronaOutput(BaseModel):
    numero_poltrona: int
    sessao: SessoesPoltronaOutput
    class Config:
        orm_mode = True
