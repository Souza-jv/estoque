from fastapi import APIRouter
from pydantic import BaseModel
from api.deps import UsuarioAtual
from produtos import servico

router = APIRouter(prefix="/produtos", tags=["Produtos e estoque"])

class QuantidadeEntrada(BaseModel):
    quantidade: int

@router.get("", summary="Listar o estoque")
def listar(quem: UsuarioAtual):
    return servico.listar(quem)

@router.post("/{codigo}/entrada", summary="Registrar entrada no estoque")
def entrada(codigo: str, dados: QuantidadeEntrada, quem: UsuarioAtual):
    return servico.entrada(quem, codigo, dados.quantidade)

@router.post("/{codigo}/saida", summary="Registrar saída no estoque")
def saida(codigo: str, dados: QuantidadeEntrada, quem: UsuarioAtual):
    return servico.saida(quem, codigo, dados.quantidade)