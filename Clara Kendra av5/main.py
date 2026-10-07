import os
from typing import List, Optional
import dotenv
from sqlalchemy import Float, ForeignKey, String, Text, create_engine, select, text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

# Carrega variáveis de ambiente do arquivo .env
dotenv.load_dotenv()


# ----------------------------------------------------------------------
# DEFINIÇÃO DOS MODELOS (ORM)
# ----------------------------------------------------------------------
class Base(DeclarativeBase):
    pass


class Espaco(Base):
    __tablename__ = "espacos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tamanho: Mapped[float] = mapped_column(Float, nullable=False)

    planetas: Mapped[List["Planeta"]] = relationship(
        back_populates="espaco", cascade="all, delete-orphan"
    )


class Planeta(Base):
    __tablename__ = "planetas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    massa: Mapped[float] = mapped_column(Float, nullable=False)
    raio: Mapped[float] = mapped_column(Float, nullable=False)

    espaco_id: Mapped[int] = mapped_column(
        ForeignKey("espacos.id"), nullable=False
    )
    espaco: Mapped["Espaco"] = relationship(back_populates="planetas")


def criar_banco_mysql_se_nao_existir(user, password, host, port, database):
    """Conecta ao MySQL sem especificar o banco e cria o schema se não existir."""
    engine_temp = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}")
    with engine_temp.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
        conn.commit()


def create_tables(engine):
    Base.metadata.create_all(engine)


# ----------------------------------------------------------------------
# FUNÇÕES DE INTERAÇÃO COM O USUÁRIO
# ----------------------------------------------------------------------
def escolher_banco():
    while True:
        print("\n=== ESCOLHA O BANCO DE DADOS ===")
        print("1 - SQLite")
        print("2 - MySQL")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            return "sqlite"
        elif opcao == "2":
            return "mysql"
        elif opcao == "0":
            return None
        else:
            print("Opção inválida.")


def inserir_espaco(session: Session):
    print("\n=== INSERIR ESPAÇO ===")

    nome = input("Nome: ")
    tipo = input("Tipo: ")
    descricao = input("Descrição: ")

    try:
        tamanho = float(input("Tamanho: "))
    except ValueError:
        print("O tamanho deve ser um número.")
        return

    espaco = Espaco(
        nome=nome, tipo=tipo, descricao=descricao, tamanho=tamanho
    )

    session.add(espaco)
    session.commit()

    print(f"Espaço inserido com sucesso! ID: {espaco.id}")


def inserir_planeta(session: Session):
    print("\n=== INSERIR PLANETA ===")

    espacos = session.scalars(select(Espaco)).all()

    if not espacos:
        print("Nenhum espaço cadastrado.")
        print("Cadastre um espaço primeiro.")
        return

    print("\nEspaços disponíveis:")
    for espaco in espacos:
        print(f"{espaco.id} - {espaco.nome}")

    try:
        espaco_id = int(input("ID do espaço: "))
    except ValueError:
        print("O ID deve ser um número.")
        return

    espaco = session.get(Espaco, espaco_id)

    if espaco is None:
        print("Espaço não encontrado.")
        return

    nome = input("Nome: ")
    tipo = input("Tipo: ")

    try:
        massa = float(input("Massa: "))
        raio = float(input("Raio: "))
    except ValueError:
        print("Massa e raio devem ser números.")
        return

    planeta = Planeta(
        nome=nome, tipo=tipo, massa=massa, raio=raio, espaco=espaco
    )

    session.add(planeta)
    session.commit()

    print(f"Planeta inserido com sucesso! ID: {planeta.id}")


def listar_espacos(session: Session):
    print("\n=== ESPAÇOS ===")

    espacos = session.scalars(select(Espaco)).all()

    if not espacos:
        print("Nenhum espaço cadastrado.")
        return

    for espaco in espacos:
        print("-------------------------")
        print(f"ID: {espaco.id}")
        print(f"Nome: {espaco.nome}")
        print(f"Tipo: {espaco.tipo}")
        print(f"Descrição: {espaco.descricao}")
        print(f"Tamanho: {espaco.tamanho}")


def listar_planetas(session: Session):
    print("\n=== PLANETAS ===")

    planetas = session.scalars(select(Planeta)).all()

    if not planetas:
        print("Nenhum planeta cadastrado.")
        return

    for planeta in planetas:
        print("-------------------------")
        print(f"ID: {planeta.id}")
        print(f"Nome: {planeta.nome}")
        print(f"Tipo: {planeta.tipo}")
        print(f"Massa: {planeta.massa}")
        print(f"Raio: {planeta.raio}")
        print(f"Espaço: {planeta.espaco.nome}")


def excluir_espaco(session: Session):
    print("\n=== EXCLUIR ESPAÇO ===")

    try:
        id_espaco = int(input("ID do espaço: "))
    except ValueError:
        print("O ID deve ser um número.")
        return

    espaco = session.get(Espaco, id_espaco)

    if espaco is None:
        print("Espaço não encontrado.")
        return

    confirmacao = input(
        f"Tem certeza que deseja excluir '{espaco.nome}'? (s/n): "
    )

    if confirmacao.lower() != "s":
        print("Exclusão cancelada.")
        return

    session.delete(espaco)
    session.commit()

    print("Espaço excluído com sucesso!")


def excluir_planeta(session: Session):
    print("\n=== EXCLUIR PLANETA ===")

    try:
        id_planeta = int(input("ID do planeta: "))
    except ValueError:
        print("O ID deve ser um número.")
        return

    planeta = session.get(Planeta, id_planeta)

    if planeta is None:
        print("Planeta não encontrado.")
        return

    confirmacao = input(
        f"Tem certeza que deseja excluir '{planeta.nome}'? (s/n): "
    )

    if confirmacao.lower() != "s":
        print("Exclusão cancelada.")
        return

    session.delete(planeta)
    session.commit()

    print("Planeta excluído com sucesso!")


def menu_operacoes(engine):
    while True:
        print("\n=== OPERAÇÕES ===")
        print("1 - Inserir espaço")
        print("2 - Inserir planeta")
        print("3 - Listar espaços")
        print("4 - Listar planetas")
        print("5 - Excluir espaço")
        print("6 - Excluir planeta")
        print("7 - Alterar banco de dados")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "0":
            return "sair"
        elif opcao == "7":
            return "trocar"

        with Session(engine) as session:
            if opcao == "1":
                inserir_espaco(session)
            elif opcao == "2":
                inserir_planeta(session)
            elif opcao == "3":
                listar_espacos(session)
            elif opcao == "4":
                listar_planetas(session)
            elif opcao == "5":
                excluir_espaco(session)
            elif opcao == "6":
                excluir_planeta(session)
            else:
                print("Opção inválida.")


def main():
    while True:
        banco = escolher_banco()

        if banco is None:
            print("Programa encerrado.")
            break

        try:
            if banco == "sqlite":
                connection_string = "sqlite:///espaco.db"
            elif banco == "mysql":
                user = os.getenv("DB_USER", "root")
                password = os.getenv("DB_PASSWORD", "")
                host = os.getenv("DB_HOST", "localhost")
                port = os.getenv("DB_PORT", "3306")
                database = os.getenv("DB_NAME", "espaco_db")

                # Garante que o banco exista no MySQL antes de conectar nele
                criar_banco_mysql_se_nao_existir(user, password, host, port, database)

                connection_string = (
                    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
                )

            engine = create_engine(connection_string)

            create_tables(engine)

            print(f"\nConectado ao banco: {banco.upper()}")

            resultado = menu_operacoes(engine)

            if resultado == "sair":
                print("Programa encerrado.")
                break
            elif resultado == "trocar":
                print("\nVoltando para escolha do banco...")

        except Exception as erro:
            print("\nErro ao conectar ou executar operações:")
            print(erro)


if __name__ == "__main__":
    main()