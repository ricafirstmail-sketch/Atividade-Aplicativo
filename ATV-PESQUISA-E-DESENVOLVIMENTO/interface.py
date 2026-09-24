import tkinter as tk
from tkinter import messagebox, ttk

from dados import adicionar_tarefa, atualizar_tarefa, buscar_tarefas, carregar_tarefas, remover_tarefa, resumo_tarefas
from validacao import validar_dados_tarefa


class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de tarefas")
        self.geometry("1100x620")
        self.minsize(900, 520)
        self.tarefa_selecionada_id = None
        self.config(bg="#f2f5f7")
        self._criar_widgets()
        self._carregar_tarefas()

    def _criar_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.lbl_titulo = ttk.Label(
            self,
            text="Gerenciador de tarefas",
            font=("Segoe UI", 16, "bold"),
            foreground="#1f2937",
        )
        self.lbl_titulo.grid(row=0, column=0, pady=(18, 10), sticky="n")

        self.lbl_resumo = ttk.Label(
            self,
            text="Resumo: 0 tarefas | 0 pendentes | 0 concluídas",
            font=("Segoe UI", 10, "bold"),
            foreground="#0f172a",
        )
        self.lbl_resumo.grid(row=1, column=0, sticky="n")

        container = ttk.Frame(self, padding=12)
        container.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        form_frame = ttk.LabelFrame(container, text="Dados da tarefa", padding=12)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky="w", pady=4)
        self.txt_titulo = ttk.Entry(form_frame, width=35)
        self.txt_titulo.grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(form_frame, text="Descrição:").grid(row=1, column=0, sticky="nw", pady=4)
        self.txt_descricao = tk.Text(form_frame, height=4, width=35)
        self.txt_descricao.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(form_frame, text="Prioridade:").grid(row=2, column=0, sticky="w", pady=4)
        self.cmb_prioridade = ttk.Combobox(
            form_frame,
            values=["baixa", "media", "alta"],
            state="readonly",
            width=32,
        )
        self.cmb_prioridade.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(form_frame, text="Prazo (DD/MM/AAAA):").grid(row=3, column=0, sticky="w", pady=4)
        self.txt_prazo = ttk.Entry(form_frame, width=35)
        self.txt_prazo.grid(row=3, column=1, sticky="ew", pady=4)

        ttk.Label(form_frame, text="Status:").grid(row=4, column=0, sticky="w", pady=4)
        self.cmb_status = ttk.Combobox(
            form_frame,
            values=["pendente", "concluida"],
            state="readonly",
            width=32,
        )
        self.cmb_status.grid(row=4, column=1, sticky="ew", pady=4)

        botoes = ttk.Frame(form_frame)
        botoes.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        botoes.columnconfigure(0, weight=1)
        botoes.columnconfigure(1, weight=1)
        botoes.columnconfigure(2, weight=1)
        botoes.columnconfigure(3, weight=1)

        self.btn_cadastrar = ttk.Button(botoes, text="Cadastrar", command=self._cadastrar_tarefa)
        self.btn_cadastrar.grid(row=0, column=0, padx=4, sticky="ew")

        self.btn_atualizar = ttk.Button(botoes, text="Atualizar", command=self._atualizar_tarefa)
        self.btn_atualizar.grid(row=0, column=1, padx=4, sticky="ew")

        self.btn_excluir = ttk.Button(botoes, text="Excluir", command=self._excluir_tarefa)
        self.btn_excluir.grid(row=0, column=2, padx=4, sticky="ew")

        self.btn_limpar = ttk.Button(botoes, text="Limpar", command=self._limpar_formulario)
        self.btn_limpar.grid(row=0, column=3, padx=4, sticky="ew")

        list_frame = ttk.LabelFrame(container, text="Lista de tarefas", padding=12)
        list_frame.grid(row=0, column=1, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)

        busca_frame = ttk.Frame(list_frame)
        busca_frame.grid(row=0, column=0, sticky="ew")
        busca_frame.columnconfigure(0, weight=1)
        ttk.Label(busca_frame, text="Buscar:").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.txt_busca = ttk.Entry(busca_frame)
        self.txt_busca.grid(row=0, column=1, sticky="ew", padx=(0, 6))
        ttk.Button(busca_frame, text="Pesquisar", command=self._buscar_tarefas).grid(row=0, column=2)

        colunas = ("id", "titulo", "prioridade", "prazo", "status")
        self.tree = ttk.Treeview(list_frame, columns=colunas, show="headings", height=18)
        self.tree.heading("id", text="ID")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("prioridade", text="Prioridade")
        self.tree.heading("prazo", text="Prazo")
        self.tree.heading("status", text="Status")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("titulo", width=220, anchor="w")
        self.tree.column("prioridade", width=100, anchor="center")
        self.tree.column("prazo", width=90, anchor="center")
        self.tree.column("status", width=110, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.tree.bind("<ButtonRelease-1>", self._selecionar_tarefa)

        self._limpar_formulario()

    def _coletar_dados_formulario(self):
        return {
            "titulo": self.txt_titulo.get(),
            "descricao": self.txt_descricao.get("1.0", "end").strip(),
            "prioridade": self.cmb_prioridade.get(),
            "prazo": self.txt_prazo.get(),
            "status": self.cmb_status.get() or "pendente",
        }

    def _atualizar_resumo(self):
        indicadores = resumo_tarefas()
        self.lbl_resumo.config(
            text=(
                f"Resumo: {indicadores['total']} tarefas | "
                f"{indicadores['pendentes']} pendentes | "
                f"{indicadores['concluidas']} concluídas"
            )
        )

    def _carregar_tarefas(self):
        tarefas = carregar_tarefas()
        self.tree.delete(*self.tree.get_children())
        for tarefa in tarefas:
            self.tree.insert(
                "",
                "end",
                values=(
                    tarefa["id"],
                    tarefa["titulo"],
                    tarefa["prioridade"],
                    tarefa["prazo"],
                    tarefa["status"],
                ),
            )
        self._atualizar_resumo()

    def _buscar_tarefas(self):
        busca = self.txt_busca.get().strip()
        tarefas = buscar_tarefas(busca)
        self.tree.delete(*self.tree.get_children())
        for tarefa in tarefas:
            self.tree.insert(
                "",
                "end",
                values=(
                    tarefa["id"],
                    tarefa["titulo"],
                    tarefa["prioridade"],
                    tarefa["prazo"],
                    tarefa["status"],
                ),
            )
        self._atualizar_resumo()

    def _limpar_formulario(self):
        self.tarefa_selecionada_id = None
        self.txt_titulo.delete(0, "end")
        self.txt_descricao.delete("1.0", "end")
        self.cmb_prioridade.set("")
        self.txt_prazo.delete(0, "end")
        self.cmb_status.set("pendente")
        self.txt_busca.delete(0, "end")
        self._carregar_tarefas()

    def _cadastrar_tarefa(self):
        dados = self._coletar_dados_formulario()
        erros = validar_dados_tarefa(dados)
        if erros:
            messagebox.showerror("Dados inválidos", "\n".join(erros), parent=self)
            return
        adicionar_tarefa(dados)
        messagebox.showinfo("Sucesso", "Tarefa cadastrada com sucesso!", parent=self)
        self._limpar_formulario()

    def _selecionar_tarefa(self, event=None):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            return
        item = self.tree.item(item_selecionado[0], "values")
        self.tarefa_selecionada_id = int(item[0])
        tarefas = carregar_tarefas()
        for tarefa in tarefas:
            if tarefa["id"] == self.tarefa_selecionada_id:
                self.txt_titulo.delete(0, "end")
                self.txt_titulo.insert(0, tarefa["titulo"])
                self.txt_descricao.delete("1.0", "end")
                self.txt_descricao.insert("1.0", tarefa["descricao"])
                self.cmb_prioridade.set(tarefa["prioridade"])
                self.txt_prazo.delete(0, "end")
                self.txt_prazo.insert(0, tarefa["prazo"])
                self.cmb_status.set(tarefa["status"])
                break

    def _atualizar_tarefa(self):
        if self.tarefa_selecionada_id is None:
            messagebox.showwarning("Seleção necessária", "Selecione uma tarefa na lista para atualizar.", parent=self)
            return
        dados = self._coletar_dados_formulario()
        erros = validar_dados_tarefa(dados)
        if erros:
            messagebox.showerror("Dados inválidos", "\n".join(erros), parent=self)
            return
        dados["id"] = self.tarefa_selecionada_id
        if not atualizar_tarefa(dados):
            messagebox.showerror("Erro", "Não foi possível atualizar a tarefa.", parent=self)
            return
        messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso!", parent=self)
        self._limpar_formulario()

    def _excluir_tarefa(self):
        if self.tarefa_selecionada_id is None:
            messagebox.showwarning("Seleção necessária", "Selecione uma tarefa para excluir.", parent=self)
            return
        confirmacao = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir a tarefa {self.tarefa_selecionada_id}?",
            parent=self,
        )
        if not confirmacao:
            return
        if not remover_tarefa(self.tarefa_selecionada_id):
            messagebox.showerror("Erro", "Não foi possível excluir a tarefa.", parent=self)
            return
        messagebox.showinfo("Sucesso", "Tarefa removida com sucesso!", parent=self)
        self._limpar_formulario()
