from sqlalchemy.orm import Session
from . import models, schemas

def get_equipamento(db: Session, equipamento_id: int):
    return db.query(models.Equipamento).filter(models.Equipamento.id == equipamento_id).first()

def get_equipamento_by_serie(db: Session, numero_serie: str):
    return db.query(models.Equipamento).filter(models.Equipamento.numero_serie == numero_serie).first()

def get_equipamento_by_patrimonio(db: Session, numero_patrimonio: str):
    return db.query(models.Equipamento).filter(models.Equipamento.numero_patrimonio == numero_patrimonio).first()

def get_equipamentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Equipamento).offset(skip).limit(limit).all()

def create_equipamento(db: Session, equipamento: schemas.EquipamentoCreate):
    db_equipamento = models.Equipamento(
        marca=equipamento.marca,
        modelo=equipamento.modelo,
        numero_serie=equipamento.numero_serie,
        numero_patrimonio=equipamento.numero_patrimonio
    )
    db.add(db_equipamento)
    db.commit()
    db.refresh(db_equipamento)
    return db_equipamento

def update_equipamento(db: Session, equipamento_id: int, equipamento: schemas.EquipamentoUpdate):
    db_equipamento = db.query(models.Equipamento).filter(models.Equipamento.id == equipamento_id).first()
    if db_equipamento:
        update_data = equipamento.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_equipamento, key, value)
        db.commit()
        db.refresh(db_equipamento)
    return db_equipamento

def delete_equipamento(db: Session, equipamento_id: int):
    db_equipamento = db.query(models.Equipamento).filter(models.Equipamento.id == equipamento_id).first()
    if db_equipamento:
        db.delete(db_equipamento)
        db.commit()
    return db_equipamento
