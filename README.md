# Sistema de Almoxarifado - Controle de Estoque

**Aluno:** [João Vitor Souza de Moraes]  
**Turma:** [Técnico em Desenvolvimento de Sistemas / Programação de Aplicativos]

Sistema em Python para controle de estoque, gerenciamento de usuários e fluxo de aprovação de solicitações de compra.

## Estrutura do Projeto

* `produtos/` — Cadastro e controle de saldo de itens do estoque.
* `usuarios/` — Gerenciamento de usuários, perfis e permissões de acesso.
* `solicitacoes/` — Controle do ciclo de vida das solicitações de compra (abertura, aprovação, andamento e cancelamento).
* `testes/` — Scripts automatizados de validação das regras de negócio.

## Como rodar os testes

No terminal, na pasta raiz do projeto, execute:

```bash
python -m testes.teste_solicitacao