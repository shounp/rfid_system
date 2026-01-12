from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    uid = Column(String(50), primary_key=True)
    nome = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Usuario(uid={self.uid}, nome={self.nome})>"


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(50), nullable=False)
    datahora = Column(DateTime, default=datetime.now)
    status = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<Log(uid={self.uid}, status={self.status}, datahora={self.datahora})>"
