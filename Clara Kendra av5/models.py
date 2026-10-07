from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Espaco(Base):
    __tablename__ = "espacos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    tamanho: Mapped[float] = mapped_column(Float, nullable=False)

    planetas: Mapped[list["Planeta"]] = relationship(
        back_populates="espaco",
        cascade="all, delete-orphan"
    )


class Planeta(Base):
    __tablename__ = "planetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    massa: Mapped[float] = mapped_column(Float, nullable=False)
    raio: Mapped[float] = mapped_column(Float, nullable=False)

    espaco_id: Mapped[int] = mapped_column(
        ForeignKey("espacos.id"),
        nullable=False
    )

    espaco: Mapped["Espaco"] = relationship(
        back_populates="planetas"
    )