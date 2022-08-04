from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, Float, DateTime

from .database import Base


class User(Base):
    __tablename__="login"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable= False, unique=True)
    senha = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))


class Animes(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True, nullable=False)
    anichart_id = Column(Integer, unique=True)
    nome = Column(String, nullable = False)
    score_anilist = Column(Integer)
    origem = Column(String)
    descricao_en = Column(String, nullable = False)
    cover_img_url = Column(String, nullable = False)
    trailer = Column(String)
    banner_cover_img_url = Column(String)
    conteudo_adulto = Column(Boolean)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))


class TipoTicket(Base):
    __tablename__ = "tipo_ticket"

    id = Column(Integer, primary_key=True, nullable=False)
    tipo = Column(String, nullable=False, unique=True)
    valor = Column(Float,  nullable=False)

class Auditorio(Base):
    __tablename__ = "auditorio"

    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String, nullable=False)
    capacidade = Column(Integer,  nullable=False)

class Sessoes(Base):
    __tablename__ = "sessoes"
    __table_args__ = (UniqueConstraint('auditorio_id', 'horario', name='1sala1horario'),)
    id = Column(Integer, primary_key=True, nullable=False)
    anime_id = Column(Integer, ForeignKey("animes.id", ondelete="CASCADE"), nullable=False)
    auditorio_id = Column(Integer, ForeignKey("auditorio.id", ondelete="CASCADE"), nullable=False)
    horario = Column(DateTime,  nullable=False)

    anime = relationship("Animes")
    auditorio = relationship("Auditorio")

class Poltronas(Base):
    __tablename__ = "poltronas"
    __table_args__ = (UniqueConstraint('numero_poltrona', 'sessoes_id', name='1numeropara1sessao'),)
    id = Column(Integer, nullable=False, primary_key=True)
    numero_poltrona = Column(Integer, nullable=False)
    sessoes_id = Column(Integer, ForeignKey("sessoes.id", ondelete="CASCADE"), nullable=False)

    sessao = relationship("Sessoes")

class Reservas(Base):
    __tablename__ = "reservas"
    id = Column(Integer, nullable=False, primary_key=True)
    user_id= Column(Integer, ForeignKey("login.id", ondelete="CASCADE"), nullable=False)
    sessao_id= Column(Integer, ForeignKey("sessoes.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))

    user = relationship("User")
    sessao = relationship("Sessoes")

class Reservas_ticket(Base):
    __tablename__ = "reserva_ticket"
    __table_args__ = (UniqueConstraint('reserva_id', 'poltrona_id', name='1poltronaPara1reserva'),)
    id = Column(Integer, nullable=False, primary_key=True)
    tipo_ticket_id = Column(Integer, ForeignKey("tipo_ticket.id", ondelete="CASCADE"), nullable=False)
    reserva_id = Column(Integer, ForeignKey("reservas.id", ondelete="CASCADE"), nullable=False)
    poltrona_id = Column(Integer, ForeignKey("poltronas.id", ondelete="CASCADE"), nullable=False)

class Slider_homepage(Base):
    __tablename__ = "carrousel_homepage"
    __table_args__ = (UniqueConstraint('posicao_slide', name='posicaoUnica'),)
    id = Column(Integer, nullable=False, primary_key=True)
    anime_id = Column(Integer, ForeignKey("animes.id", ondelete="CASCADE"), nullable=False)
    posicao_slide = Column(Integer, nullable=False)
