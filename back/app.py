from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Paciente
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info) 
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente", description="Adição, visualização, edição e remoção de pacientes à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/paciente', tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_paciente(form: PacienteSchema):
    """Adiciona um novo Paciente à base de dados

    Retorna uma representação dos pacientes e informações associados.
    """
    paciente = Paciente(
        nome=form.nome,
        valor=form.valor,
        diadasemana=form.diadasemana,
        comentario=form.comentario)
    logger.debug(f"Adicionando paciente de nome: '{paciente.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando paciente
        session.add(paciente)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado paciente de nome: '{paciente.nome}'")
        return apresenta_paciente(paciente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Paciente de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": ListagemPacientesSchema, "404": ErrorSchema})
def get_pacientes():
    """Faz a busca por todos os Paciente cadastrados

    Retorna uma representação da listagem de pacientes.
    """
    logger.debug(f"Coletando pacientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pacientes = session.query(Paciente).all()

    if not pacientes:
        # se não há pacientes cadastrados
        return {"pacientes": []}, 200
    else:
        logger.debug(f"%d pacientes econtrados" % len(pacientes))
        # retorna a representação de paciente
        print(pacientes)
        return apresenta_pacientes(pacientes), 200


@app.get('/paciente', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):
    """Faz a busca por um Paciente a partir do nome do paciente

    Retorna uma representação dos pacientes e informações
    """
    paciente_nome = unquote(unquote(query.nome))
    print(paciente_nome)
    logger.debug(f"Coletando dados sobre paciente #{paciente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paciente = session.query(Paciente).filter(Paciente.nome == paciente_nome).first()

    if not paciente:
        # se o paciente não foi encontrado
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao buscar paciente '{paciente.nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Paciente econtrado: '{paciente.nome}'")
        # retorna a representação de paciente
        return apresenta_paciente(paciente), 200


@app.delete('/paciente', tags=[paciente_tag],
            responses={"200": PacienteDelSchema, "404": ErrorSchema})
def del_paciente(query: PacienteBuscaSchema):
    """Deleta um Paciente a partir do nome de paciente informado

    Retorna uma mensagem de confirmação da remoção.
    """
    paciente_nome = unquote(unquote(query.nome))
    print(paciente_nome)
    logger.debug(f"Deletando dados sobre paciente #{paciente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Paciente).filter(Paciente.nome == paciente_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado paciente #{paciente_nome}")
        return {"mesage": "Paciente removido", "nome": paciente_nome}
    else:
        # se o paciente não foi encontrado
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente #'{paciente_nome}', {error_msg}")
        return {"mesage": error_msg}, 404