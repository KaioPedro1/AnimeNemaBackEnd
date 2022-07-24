from typing import List, Optional
from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import schemas, database, models

router = APIRouter(
    prefix="/tickettype",
    tags = ['Ticket']
)


@router.get("/", response_model=List[schemas.TicketTypeOutput])
def get_all_ticket_type(db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    tipo_ticket = db.query(models.TipoTicket).filter(models.TipoTicket.tipo.contains(search)).limit(limit).offset(skip).all()
    return (tipo_ticket)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.TicketTypeOutput)
def inserir_tipo_ticket(ticket_input: schemas.TicketTypeBase, db: Session = Depends(database.get_db)):
    novo_tipo_ticket = models.TipoTicket(**ticket_input.dict())
    db.add(novo_tipo_ticket)
    db.commit()
    db.refresh(novo_tipo_ticket)
    return novo_tipo_ticket

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_tipo_ticket(id: int, db: Session = Depends(database.get_db)):
    tipo_ticket_query = db.query(models.TipoTicket).filter(models.TipoTicket.id == id)
    if not tipo_ticket_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar o tipo de ticket que possui Id({id}) no banco de dados")
    tipo_ticket_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.TicketTypeOutput)
def atualizar_anime(id: int, ticket_atualizado: schemas.TicketTypeBase, db: Session = Depends(database.get_db)):
    ticket_query = db.query(models.TipoTicket).filter(models.TipoTicket.id == id)
    ticket= ticket_query.first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar o ticket Id({id}) no banco de dados")
    ticket_query.update(ticket_atualizado.dict(), synchronize_session=False)
    db.commit()
    return (ticket)