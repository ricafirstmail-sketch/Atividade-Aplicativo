# Evidências do projeto

## Execução e validação
- Comando: `python -m unittest discover -s tests -v`
- Resultado: 8 testes executados e aprovados.
- Casos cobertos: cadastro, campos obrigatórios, prioridade, data, pesquisa,
  edição, exclusão, resumo e persistência.

## Roteiro da demonstração
1. Abrir com `python main.py` e apresentar o formulário.
2. Cadastrar uma tarefa válida e mostrar o resumo atualizado.
3. Tentar salvar campo vazio e data inválida para demonstrar as mensagens.
4. Selecionar a tarefa, alterar o status e atualizar.
5. Pesquisar por uma palavra e excluir confirmando a operação.
6. Fechar e abrir novamente para comprovar a persistência em JSON.

## Registro de falhas e correções
Não foram identificadas falhas pendentes nos testes automatizados. A validação foi mantida
em módulo separado para impedir que dados inválidos chegassem à persistência.

