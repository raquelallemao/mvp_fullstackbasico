from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Paciente(Base):
    __tablename__ = 'paciente'

    id = Column ("pk_paciente", Integer, primary_key=True)
    nome = Column (String(140), unique=True)
    valor = Column (Float)
    diadasemana = Column (String(140))
    comentario = Column (String(300))
    data_insercao = Column(DateTime, default=datetime.now())
