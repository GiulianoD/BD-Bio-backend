from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Equipamento(Base):
    __tablename__ = "equipamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    numero_serie = Column(String(50), unique=True, nullable=False, index=True)
    numero_patrimonio = Column(String(50), unique=True, nullable=False, index=True)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Equipamento {self.marca} {self.modelo} - {self.numero_serie}>"
    