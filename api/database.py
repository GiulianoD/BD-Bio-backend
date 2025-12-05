from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Para lidar com caracteres especiais na senha
if DATABASE_URL:
    from urllib.parse import quote_plus
    # Codificar partes da URL se necessário
    if "EvlDB*2019" in DATABASE_URL:
        # Substituir a senha pela versão codificada
        parts = DATABASE_URL.split("://")
        if len(parts) == 2:
            user_pass_host = parts[1].split("@")
            if len(user_pass_host) == 2:
                user_pass = user_pass_host[0]
                host_db = user_pass_host[1]
                user, password = user_pass.split(":")
                encoded_password = quote_plus(password)
                DATABASE_URL = f"{parts[0]}://{user}:{encoded_password}@{host_db}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
