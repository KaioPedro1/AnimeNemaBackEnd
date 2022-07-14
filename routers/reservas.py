from typing import List, Optional
from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import schemas, database, models

router = APIRouter(
    prefix="/reservas"
)


@router.get("/", response_model=List[schemas.ReservaOutput])
def get_all_reservas(db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0):
    reserva = db.query(models.Reservas).limit(limit).offset(skip).all()
    return (reserva)
#
@router.get("/{id}", response_model=List[schemas.ReservaTicketOutput])
def get_reservas_ticket(id: int, db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0):
    reserva_ticket = db.query(models.Reservas_ticket.id, models.Reservas_ticket.reserva_id,
                              models.Poltronas.numero_poltrona, models.TipoTicket.tipo,
                              models.TipoTicket.valor).\
        outerjoin(models.TipoTicket, models.Reservas_ticket.tipo_ticket_id == models.TipoTicket.id).\
        outerjoin(models.Poltronas, models.Reservas_ticket.poltrona_id == models.Poltronas.id).\
        filter(models.Reservas_ticket.reserva_id == id).\
        limit(limit).offset(skip).all()
    if not reserva_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel encontrar ({id}), pedido inexistente ou pedido nao possui tickets")
    return (reserva_ticket)

@router.post("/ticket", status_code = status.HTTP_201_CREATED)
def inserir_reserva_ticket(reserva_ticket_input: schemas.ReservaTicketBase, db: Session = Depends(database.get_db)):
    nova_reserva_ticket = models.Reservas_ticket(**reserva_ticket_input.dict())
    try:
        db.add(nova_reserva_ticket)
        db.commit()
        db.refresh(nova_reserva_ticket)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Não foi possivel inserir ticket no servidor, revise os dados inseridos")
    return nova_reserva_ticket

@router.post("/", status_code = status.HTTP_201_CREATED)
def inserir_reserva(reserva_input: schemas.ReservaBase, db: Session = Depends(database.get_db)):
    nova_reserva = models.Reservas(**reserva_input.dict())
    try:
        db.add(nova_reserva)
        db.commit()
        db.refresh(nova_reserva)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Não foi possivel inserir dados no servidor, revise os dados inseridos")
    return nova_reserva

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_reserva(id: int, db: Session = Depends(database.get_db)):
    reserva_query = db.query(models.Reservas).filter(models.Reservas.id == id)
    if not reserva_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel deletar a reserva Id({id}), id inexistente")
    reserva_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.delete("/ticket/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_reserva_ticket(id: int, db: Session = Depends(database.get_db)):
    reserva_query = db.query(models.Reservas_ticket).filter(models.Reservas_ticket.id == id)
    if not reserva_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possivel deletar o ticket ({id}), id inexistente")
    reserva_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
