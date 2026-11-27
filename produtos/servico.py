from api.erros import nao_encontrado, proibido, recusado
from produtos import repositorio as repo

def listar(quem):
    if not quem.pode("ver_produtos"):
        raise proibido()
    return repo.almoxarifado().listar()

def entrada(quem, codigo, qtd):
    if not quem.pode("movimentar_estoque"):
        raise proibido("Só o almoxarifado movimenta o estoque.")
    if qtd <= 0:
        raise recusado("A quantidade precisa ser maior que zero.")

    almox = repo.almoxarifado()
    if not almox.entrada(codigo, qtd):
        raise nao_encontrado("Produto não encontrado.")

    produto = repo.buscar(codigo)
    return produto.listar_produtos()

def saida(quem, codigo, qtd):
    if not quem.pode("movimentar_estoque"):
        raise proibido("Só o almoxarifado movimenta o estoque.")

    produto = repo.buscar(codigo)
    if not produto:
        raise nao_encontrado("Produto não encontrado.")

    if not produto.saida(qtd):
        raise recusado("Saldo insuficiente: há " + str(produto.quantidade) + " em estoque.")

    return produto.listar_produtos()