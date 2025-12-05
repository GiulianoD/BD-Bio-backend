from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import crud, models, schemas
from .database import engine, get_db

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Cadastro de Equipamentos",
    description="API para gerenciar equipamentos do sistema",
    version="1.0.0"
)

# Configuração CORS para permitir requisições do seu HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "file://"],  # Adicione a origem do seu HTML
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API de Cadastro de Equipamentos"}

@app.post("/equipamentos/", response_model=schemas.Equipamento, status_code=status.HTTP_201_CREATED)
def criar_equipamento(equipamento: schemas.EquipamentoCreate, db: Session = Depends(get_db)):
    # Verifica se número de série já existe
    db_equipamento = crud.get_equipamento_by_serie(db, numero_serie=equipamento.numero_serie)
    if db_equipamento:
        raise HTTPException(
            status_code=400,
            detail="Número de série já cadastrado"
        )
    
    # Verifica se número de patrimônio já existe
    db_equipamento = crud.get_equipamento_by_patrimonio(db, numero_patrimonio=equipamento.numero_patrimonio)
    if db_equipamento:
        raise HTTPException(
            status_code=400,
            detail="Número de patrimônio já cadastrado"
        )
    
    return crud.create_equipamento(db=db, equipamento=equipamento)

@app.get("/equipamentos/", response_model=List[schemas.Equipamento])
def listar_equipamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    equipamentos = crud.get_equipamentos(db, skip=skip, limit=limit)
    return equipamentos

@app.get("/equipamentos/{equipamento_id}", response_model=schemas.Equipamento)
def ler_equipamento(equipamento_id: int, db: Session = Depends(get_db)):
    db_equipamento = crud.get_equipamento(db, equipamento_id=equipamento_id)
    if db_equipamento is None:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    return db_equipamento

@app.put("/equipamentos/{equipamento_id}", response_model=schemas.Equipamento)
def atualizar_equipamento(equipamento_id: int, equipamento: schemas.EquipamentoUpdate, db: Session = Depends(get_db)):
    db_equipamento = crud.update_equipamento(db, equipamento_id=equipamento_id, equipamento=equipamento)
    if db_equipamento is None:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    return db_equipamento

@app.delete("/equipamentos/{equipamento_id}", response_model=schemas.Equipamento)
def deletar_equipamento(equipamento_id: int, db: Session = Depends(get_db)):
    db_equipamento = crud.delete_equipamento(db, equipamento_id=equipamento_id)
    if db_equipamento is None:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    return db_equipamento

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
