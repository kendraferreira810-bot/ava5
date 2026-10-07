import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.models import Base


load_dotenv()


def criar_engine(tipo_banco):
    if tipo_banco == "sqlite":
        return create_engine("sqlite:///av5.db")

    if tipo_banco == "mysql":
        usuario = os.getenv("MYSQL_USER")
        senha = os.getenv("MYSQL_PASSWORD")
        host = os.getenv("MYSQL_HOST")
        porta = os.getenv("MYSQL_PORT")
        banco = os.getenv("MYSQL_DATABASE")

        url = (
            f"mysql+pymysql://{usuario}:{senha}"
            f"@{host}:{porta}/{banco}"
        )

        return create_engine(url)

    raise ValueError("Banco de dados inválido.")


def criar_tabelas(engine):
    Base.metadata.create_all(engine)