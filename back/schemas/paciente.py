from pydantic import BaseModel
from typing import Optional, List
from model.paciente import Paciente


class PacienteSchema(BaseModel):
    nome: str = "João"
    valor: Optional[float] = 120.00
    diadasemana: str = "Quarta-feira"
    comentario: str = "Atendimento Presencial"


class PacienteBuscaSchema(BaseModel):
    nome: str = "João"


class ListagemPacientesSchema(BaseModel):
    pacientes:List[PacienteSchema]


def apresenta_pacientes(pacientes: List[Paciente]):
    result = []
    for paciente in pacientes:
        result.append({
            "nome": paciente.nome,
            "valor": paciente.valor,
            "diadasemana": paciente.diadasemana,
            "comentario": paciente.comentario,
        })

    return {"paciente": result}


class PacienteViewSchema(BaseModel):
    id: int = 1
    nome: str = "João"
    valor: Optional[float] = 120.00
    diadasemana: str = "Quarta-feira"
    comentario: str = "Atendimento Presencial"


class PacienteDelSchema(BaseModel):
    msg: str
    nome: str

def apresenta_paciente(paciente: Paciente):
    return {
        "id": paciente.id,
        "nome": paciente.nome,
        "valor": paciente.valor,
        "diadasemana": paciente.diadasemana,
        "comentario": paciente.comentario,
    }