# Gerenciador de tarefas

## Visão geral
Aplicativo desktop em Python e Tkinter para cadastro, consulta, edição e exclusão de
tarefas. Os dados são validados e persistidos em JSON.

## Pesquisa orientada sobre Tkinter
1. **O que é Tkinter e qual sua relação com Python e Tcl/Tk?**  
   Tkinter é a biblioteca padrão do Python para interfaces gráficas e funciona como ponte
   para o toolkit Tcl/Tk. `tk.Tk` cria a janela e `ttk` fornece widgets com aparência nativa.
2. **O que caracteriza uma aplicação orientada a eventos?**  
   O programa aguarda ações do usuário e executa callbacks associados. O `mainloop()` mantém
   a janela aberta e distribui cliques, seleções e teclas.
3. **O que são widgets?**  
   São componentes visuais. O projeto usa `Label`, `Entry`, `Text`, `Button`, `Frame`,
   `Combobox` e `Treeview` para textos, entradas, ações, escolhas e listagem.
4. **Compare pack, grid e place.**  
   `pack` organiza blocos, `grid` usa linhas e colunas e `place` usa coordenadas. Foi usado
   `grid` por combinar com a estrutura do formulário e da tabela. Não se deve misturar
   `pack` e `grid` no mesmo container porque os gerenciadores podem conflitar.
5. **O que são callbacks?**  
   São funções acionadas por eventos. Por exemplo, `command=self._cadastrar_tarefa` chama
   o cadastro no clique e `tree.bind` trata a seleção de uma linha.
6. **Para que servem StringVar, IntVar, DoubleVar e BooleanVar?**  
   Essas variáveis conectam valores aos widgets. Neste projeto os métodos dos próprios
   widgets foram suficientes porque os campos são simples e textuais.
7. **Como validar obrigatórios, datas e limites?**  
   Os valores são normalizados, os campos são conferidos, a prioridade deve ser baixa,
   media ou alta e o prazo deve ser uma data real no formato `DD/MM/AAAA`.
8. **Como usar messagebox, filedialog e ttk?**  
   `messagebox` informa erros, sucessos e confirma exclusões; `ttk` fornece widgets
   consistentes. `filedialog` seria usado para escolher arquivos, mas o projeto mantém um
   JSON local para simplificar a instalação.
9. **Compare JSON, CSV e SQLite.**  
   JSON é legível e preserva registros estruturados, por isso atende este pequeno aplicativo.
   CSV é melhor para tabelas e exportação; SQLite é melhor para consultas, integridade e
   volumes maiores.
10. **Quais cuidados de usabilidade e acessibilidade existem?**  
    Há rótulos claros, ordem visual lógica, botões nomeados, mensagens compreensíveis,
    janela redimensionável e seleção da tabela para editar sem redigitação.
11. **Quais vantagens e limitações do Tkinter?**  
    É incluído no Python, simples, multiplataforma e adequado para CRUDs pequenos. Seus
    widgets são mais básicos que os de frameworks modernos e exigem mais trabalho em telas
    grandes.
12. **Como distribuir o programa?**  
    Deve-se enviar a pasta, instalar Python 3 com Tkinter e executar `python main.py`.
    Para usuários sem Python, PyInstaller pode gerar um executável, incluindo o JSON.

## Proposta do projeto
- **Problema:** organizar compromissos e pendências por prioridade e prazo.
- **Público:** estudantes e profissionais.
- **Dados:** id, título, descrição, prioridade, prazo e status.
- **Funcionalidades:** cadastrar, listar, pesquisar, editar, excluir, limpar e resumir.
- **Telas:** formulário de cadastro/edição e área de consulta com busca.
- **Persistência:** `dados/tarefas.json`.
- **Maior risco:** manter o JSON consistente; leitura, escrita e normalização ficam
  centralizadas em `dados.py`.

## Dicionário de dados
| Campo | Tipo | Validação | Obrigatório | Exemplo |
|---|---|---|---|---|
| id | inteiro | gerado automaticamente | sim | 1 |
| titulo | texto | não vazio | sim | Estudar Python |
| descricao | texto | não vazio | sim | Revisar Tkinter |
| prioridade | texto | baixa, media ou alta | sim | alta |
| prazo | texto | data DD/MM/AAAA | sim | 30/09/2026 |
| status | texto | pendente ou concluida | sim | pendente |

## Arquitetura
- `main.py`: ponto de entrada.
- `interface.py`: widgets, navegação, eventos e mensagens.
- `dados.py`: persistência e operações CRUD em JSON.
- `validacao.py`: regras de campos e formatos.
- `dados/tarefas.json`: armazenamento local.

## Plano e registro de testes
| ID | Cenário | Resultado esperado | Resultado obtido | Situação |
|---|---|---|---|---|
| CT01 | Cadastrar tarefa válida | Registro salvo e listado | Conforme esperado | Aprovado |
| CT02 | Campo obrigatório vazio | Cadastro bloqueado com aviso | Conforme esperado | Aprovado |
| CT03 | Prioridade inválida | Erro de validação | Conforme esperado | Aprovado |
| CT04 | Data inválida | Erro de validação | Conforme esperado | Aprovado |
| CT05 | Pesquisar por título | Só resultados correspondentes | Conforme esperado | Aprovado |
| CT06 | Editar tarefa selecionada | Dados atualizados | Conforme esperado | Aprovado |
| CT07 | Excluir tarefa confirmada | Registro removido | Conforme esperado | Aprovado |
| CT08 | Reabrir após salvar | Dados preservados | Conforme esperado | Aprovado |

Comando: `python -m unittest discover -s tests -v`  
Resultado: 8 testes executados, todos aprovados.

## Demonstração
Abrir com `python main.py`, cadastrar uma tarefa, demonstrar uma validação inválida,
pesquisar, editar o status, excluir confirmando e reabrir para comprovar a persistência.

## Fontes
- [Documentação oficial do tkinter](https://docs.python.org/3/library/tkinter.html) —
  Python Software Foundation.
- [Documentação oficial do ttk](https://docs.python.org/3/library/tkinter.ttk.html) —
  Python Software Foundation.
- [Documentação oficial do json](https://docs.python.org/3/library/json.html) —
  Python Software Foundation.
- [Documentação de datetime](https://docs.python.org/3/library/datetime.html) —
  Python Software Foundation.
- SENAI — Atividade prática de desenvolvimento de software desktop.
