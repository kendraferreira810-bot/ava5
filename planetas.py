from sqlalchemy import create_engine, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List
import os
from dotenv import load_dotenv


class Base(DeclarativeBase):
    pass


class Espaco(Base):
    __tablename__ = "tabela_espaco"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    localizacao: Mapped[str] = mapped_column(Text)
    descricao: Mapped[str] = mapped_column(Text)

    planetas: Mapped[List["PlanetasNoEspaco"]] = relationship(
        back_populates="espaco"
    )


class Planetas(Base):
    __tablename__ = "tabela_planetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    tamanho: Mapped[str] = mapped_column(String(30))
    tipo: Mapped[str] = mapped_column(String(30))

    espaco: Mapped[List["PlanetasNoEspaco"]] = relationship(
        back_populates="planeta"
    )


class PlanetasNoEspaco(Base):
    __tablename__ = "tabela_planetas_no_espaco"

    # chave estrangeira
    Planetas_id: Mapped[int] = mapped_column(
        ForeignKey("tabela_planetas.id"),
        primary_key=True
    )

    # chave estrangeira
    Espaco_id: Mapped[int] = mapped_column(
        ForeignKey("tabela_espaco.id"),
        primary_key=True
    )

    # atributos de acesso ao objeto
    planeta: Mapped["Planetas"] = relationship(
        back_populates="espaco"
    )

    espaco: Mapped["Espaco"] = relationship(
        back_populates="planetas"
    )

    nome_cientifico: Mapped[str] = mapped_column(String(250))
    composicao: Mapped[str] = mapped_column(String(250))


load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

print("Escolha um banco:")
print("1 - MySQL")
print("2 - SQLite")

opcao = input("Digite sua opção: ")

if opcao == "1":
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

elif opcao == "2":
    engine = create_engine("sqlite:///espaco.db")

else:
    print("Opção inválida!")
    exit()

Base.metadata.create_all(engine)

with Session(engine) as session:

    e1 = Espaco(
        nome="Sistema Solar",
        localizacao="Via Láctea",
        descricao="Sistema planetário formado pelo Sol e corpos celestes."
    )

    p1 = Planetas(
        nome="Terra",
        tamanho="médio",
        tipo="rochoso"
    )

    p2 = Planetas(
        nome="Júpiter",
        tamanho="grande",
        tipo="gasoso"
    )

    p3 = Planetas(
        nome="Marte",
        tamanho="pequeno",
        tipo="rochoso"
    )

    p4 = Planetas(
        nome="Netuno",
        tamanho="grande",
        tipo="gigante de gelo"
    )

    pe1 = PlanetasNoEspaco(
        planeta=p1,
        espaco=e1,
        nome_cientifico="Terra",
        composicao="Rochas, metais e água"
    )

    pe2 = PlanetasNoEspaco(
        planeta=p2,
        espaco=e1,
        nome_cientifico="Jupiter",
        composicao="Hidrogênio e hélio"
    )

    pe3 = PlanetasNoEspaco(
        planeta=p3,
        espaco=e1,
        nome_cientifico="Mars",
        composicao="Rochas e óxidos de ferro"
    )

    pe4 = PlanetasNoEspaco(
        planeta=p4,
        espaco=e1,
        nome_cientifico="Neptunus",
        composicao="Gelo, água, amônia e metano"
    )

    # adiciona o espaço e os objetos relacionados
    session.add(e1)

    # salva tudo
    session.commit()

    print("As tabelas foram criadas e os dados foram inseridos.")
    print(
        f"O espaço chamado {e1.nome} foi salvo sob o número {e1.id}."
    )

    print("Planetas no Espaço:")

    for item in e1.planetas:
        print(
            item.planeta.nome,
            item.nome_cientifico,
            item.composicao
        )
        # commit da Clara !!!!!!!!!!!!!!! :)