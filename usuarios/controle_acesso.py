# controle_acesso.py — a classe ControleAcesso guarda os usuários e cuida do login
# É a mesma ideia da Almoxarifado: uma classe que guarda uma lista de objetos.
import secrets

from usuarios.papeis import papeis_validos

# A mesma mensagem para matrícula que não existe e senha errada:
# se fossem diferentes, daria para descobrir quais matrículas existem.
CREDENCIAL_INVALIDA = "Matrícula ou senha inválida."


class ControleAcesso:
    # Construtor: começa sem usuários e sem ninguém logado
    def __init__(self):
        self.usuarios = []
        self.sessoes = {}           # token → matrícula de quem está logado

    # Devolve o Usuario com essa matrícula, ou None
    def buscar(self, matricula):
        for u in self.usuarios:
            if u.matricula == matricula:
                return u
        return None

    # Guarda um usuário novo; False se a matrícula já existe
    def cadastrar(self, usuario):
        achado = self.buscar(usuario.matricula)
        if achado is not None:
            return False
        self.usuarios.append(usuario)
        return True

    # Faz o login: devolve um token, ou None se algo estiver errado
    def entrar(self, matricula, senha):
        usuario = self.buscar(matricula)
        # Matrícula inexistente, senha errada e usuário não ativo
        # dão a mesma resposta (None), para não revelar quais matrículas existem
        if usuario is None:
            return None
        if not usuario.conferir_senha(senha):
            return None
        if usuario.situacao != "ativo":
            return None
        # Tudo certo: cria o token (a "pulseira") e guarda de quem ele é
        token = secrets.token_hex(16)
        self.sessoes[token] = matricula
        return token

    # Devolve o Usuario dono do token, ou None se o token não existir
    def usuario_logado(self, token):
        matricula = self.sessoes.get(token)
        if matricula is None:
            return None
        return self.buscar(matricula)

    # Encerra a sessão: apaga o token; False se ele não existir
    def sair(self, token):
        if token not in self.sessoes:
            return False
        del self.sessoes[token]
        return True

    # Troca os papéis de alguém; None se deu certo, ou o texto com o motivo da recusa
    def mudar_papeis(self, quem, matricula, papeis):
        # 1. quem está pedindo precisa ter permissão
        if not quem.pode("mudar_papeis"):
            return "Você não tem permissão para mudar papéis."
        # 2. a matrícula precisa existir
        alvo = self.buscar(matricula)
        if alvo is None:
            return "Usuário não encontrado."
        # 3. a lista não pode vir vazia
        if len(papeis) == 0:
            return "Escolha pelo menos um papel."
        # 4. todos os papéis precisam ser válidos
        for papel in papeis:
            if papel not in papeis_validos():
                return "Papel inválido: " + papel
        # Tudo certo: troca os papéis
        alvo.papeis = papeis
        return None