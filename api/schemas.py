from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EquipamentoBase(BaseModel):
    marca: str = Field(..., max_length=100)
    modelo: str = Field(..., max_length=100)
    numero_serie: str = Field(..., max_length=50)
    numero_patrimonio: str = Field(..., max_length=50)

class EquipamentoCreate(EquipamentoBase):
    pass

class EquipamentoUpdate(BaseModel):
    marca: Optional[str] = Field(None, max_length=100)
    modelo: Optional[str] = Field(None, max_length=100)
    numero_serie: Optional[str] = Field(None, max_length=50)
    numero_patrimonio: Optional[str] = Field(None, max_length=50)

class Equipamento(EquipamentoBase):
    id: int
    data_cadastro: datetime
    data_atualizacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True
