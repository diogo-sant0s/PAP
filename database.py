from sqlalchemy import create_engine, Column, String, inspect, DateTime, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime
import uuid

db = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Colaborador(Base):
    __tablename__ = "Colaborador"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    registros = relationship("Acesso", back_populates="colaborador")

class Acesso(Base):
    __tablename__ = "Acesso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, default=datetime.datetime.utcnow)
    acao = Column(String)
    colaborador_id = Column(String, ForeignKey("Colaborador.id"))  

    colaborador = relationship("Colaborador", back_populates="registros")

Base.metadata.create_all(bind=db)

# Inspect columns
inspector = inspect(db)
columns = [col['name'] for col in inspector.get_columns('Colaborador')]
print(columns)
