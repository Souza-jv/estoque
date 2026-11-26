class Almoxarifado:
    # Construtor: o almoxarifado nasce com o nome da unidade e sem produtos
    def __init__(self, unidade):
        self.unidade = unidade
        self.produtos = []

    # Guarda um objeto Produto no fim da lista
    def adicionar(self, produto):
        self.produtos.append(produto)

    # Conta quantos produtos estão com quantidade zero
    def contar_em_falta(self):
        total = 0

        for p in self.produtos:
            if p.situacao() == "Em falta":
                total += 1

        return total

    # 1. Devolve o Produto que tem o código informado, ou None se não achar
    def buscar(self, codigo):
        for p in self.produtos:
            if p.codigo == codigo:
                return p
        return None

    # 2. Registra a entrada de um produto; False se o código não existe
    def entrada(self, codigo, qtd):
        p = self.buscar(codigo)
        if p is None:
            return False
        p.entrada(qtd)
        return True

    # 3. Registra a saída de um produto; devolve o resultado do Produto
    def saida(self, codigo, qtd):
        p = self.buscar(codigo)
        if p is None:
            return False
        return p.saida(qtd)

    # 4. Devolve uma lista de dicionários, um por produto
    def listar(self):
        lista = []
        for p in self.produtos:
            lista.append(p.listar_produtos())
        return lista

    # 5. Devolve só os produtos que não estão OK (Repor ou Em falta)
    def solicitacao_compra(self):
        pedido = []
        for p in self.produtos:
            if p.situacao() != "OK":
                pedido.append({
                    "codigo": p.codigo,
                    "nome": p.nome,
                    "situacao": p.situacao(),
                })
        return pedido

    # 6. Devolve a soma de quantidade x preço de todos os produtos
    def valor_estoque(self):
        total = 0
        for p in self.produtos:
            total += p.quantidade * p.preco
        return total

    # 7. Devolve o almoxarifado inteiro em um dicionário
    def para_dicionario(self):
        return {
            "unidade": self.unidade,
            "total_produtos": len(self.produtos),
            "produtos": self.listar(),
        }