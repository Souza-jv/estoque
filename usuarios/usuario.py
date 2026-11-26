# usuario.py — a classe Usuario: quem é a pessoa e o que ela pode fazer
# A senha nunca fica guardada como foi digitada: guardamos só o resumo (hash).

import hashlib
import secrets

from usuarios.papeis import PERMISSOES


class Usuario:
    # Construtor: matrícula, nome, senha e a lista de papéis
    def __init__(self, matricula, nome, senha, papeis, supervisor=None):
        self.matricula = matricula
        self.nome = nome
        self.papeis = papeis                # ex.: ["solicitante", "supervisor"]
        self.supervisor = supervisor        # matrícula de quem aprova os pedidos dele
        self.situacao = "ativo"             # pendente, ativo, recusado ou inativo
        # O _ na frente avisa: atributo interno, ninguém de fora mexe
        self._sal = secrets.token_hex(8)
        self._senha_hash = self._resumir(senha)

    # Transforma a senha em um resumo que não dá para desfazer
    def _resumir(self, senha):
        texto = (self._sal + senha).encode("utf-8")
        return hashlib.sha256(texto).hexdigest()

    # True se a senha digitada bate com a guardada
    def conferir_senha(self, senha):
        return self._resumir(senha) == self._senha_hash

    # True se a pessoa tem esse papel
    def tem_papel(self, papel):
        return papel in self.papeis

    # True se algum dos cargos da pessoa tem essa permissão
    # Se a situação não for "ativo", devolve False para qualquer permissão
    def pode(self, permissao):
        # Cadastro pendente, recusado ou inativo não pode nada
        if self.situacao != "ativo":
            return False
        # Para cada cargo da pessoa, procura a permissão na lista dele
        for papel in self.papeis:
            if permissao in PERMISSOES.get(papel, []):
                return True
        return False

    # Lista com as permissões de todos os cargos, sem repetir, na ordem em que aparecem
    def permissoes(self):
        lista = []
        for papel in self.papeis:
            for permissao in PERMISSOES.get(papel, []):
                # Só adiciona se ainda não está na lista (evita repetição)
                if permissao not in lista:
                    lista.append(permissao)
        return lista

    # Só troca a senha se a atual estiver certa
    # Devolve True quando trocou e False quando a senha atual está errada
    def trocar_senha(self, atual, nova):
        if not self.conferir_senha(atual):
            return False
        # A senha nova também é guardada como resumo
        self._senha_hash = self._resumir(nova)
        return True

    # Dicionário com os dados da pessoa, pronto para a API enviar
    # A senha e o resumo nunca entram aqui
    def para_dicionario(self):
        return {
            "matricula": self.matricula,
            "nome": self.nome,
            "papeis": self.papeis,
            "permissoes": self.permissoes(),
            "supervisor": self.supervisor,
            "situacao": self.situacao,
        }