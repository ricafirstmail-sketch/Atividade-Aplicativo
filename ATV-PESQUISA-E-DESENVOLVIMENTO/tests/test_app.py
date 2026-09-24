import tempfile
import unittest
from pathlib import Path

from dados import adicionar_tarefa, atualizar_tarefa, buscar_tarefas, carregar_tarefas, remover_tarefa, resumo_tarefas
from validacao import validar_dados_tarefa, validar_data, validar_prioridade


class TestValidacao(unittest.TestCase):
    def test_campos_obrigatorios(self):
        dados = {"titulo": "", "descricao": "", "prioridade": "", "prazo": ""}
        erros = validar_dados_tarefa(dados)
        self.assertTrue(any("Título" in erro for erro in erros))
        self.assertTrue(any("Descrição" in erro for erro in erros))
        self.assertTrue(any("Prioridade" in erro for erro in erros))
        self.assertTrue(any("Prazo" in erro for erro in erros))

    def test_prioridade_valida(self):
        self.assertTrue(validar_prioridade("alta"))
        self.assertTrue(validar_prioridade("media"))
        self.assertTrue(validar_prioridade("baixa"))
        self.assertFalse(validar_prioridade("urgente"))

    def test_data_valida(self):
        self.assertTrue(validar_data("31/12/2025"))
        self.assertFalse(validar_data("2025-12-31"))
        self.assertFalse(validar_data("99/99/9999"))


class TestDados(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.arquivo = Path(self.temp_dir.name) / "tarefas.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_adicionar_e_listar_tarefas(self):
        tarefa = {
            "titulo": "Estudar Python",
            "descricao": "Revisar módulos e testes",
            "prioridade": "alta",
            "prazo": "20/09/2026",
            "status": "pendente",
        }
        nova = adicionar_tarefa(tarefa, caminho=self.arquivo)
        tarefas = carregar_tarefas(caminho=self.arquivo)
        self.assertEqual(len(tarefas), 1)
        self.assertEqual(nova["titulo"], "Estudar Python")
        self.assertEqual(tarefas[0]["id"], 1)

    def test_buscar_tarefas_por_texto(self):
        adicionar_tarefa({"titulo": "Estudar Python", "descricao": "Módulos", "prioridade": "alta", "prazo": "20/09/2026", "status": "pendente"}, caminho=self.arquivo)
        adicionar_tarefa({"titulo": "Organizar casa", "descricao": "Limpeza", "prioridade": "baixa", "prazo": "21/09/2026", "status": "pendente"}, caminho=self.arquivo)
        resultados = buscar_tarefas("estudar", caminho=self.arquivo)
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]["titulo"], "Estudar Python")

    def test_atualizar_tarefa(self):
        tarefa = adicionar_tarefa({"titulo": "Lavar carro", "descricao": "Completo", "prioridade": "media", "prazo": "15/10/2026", "status": "pendente"}, caminho=self.arquivo)
        tarefa["titulo"] = "Lavar carro e moto"
        tarefa["status"] = "concluida"
        sucesso = atualizar_tarefa(tarefa, caminho=self.arquivo)
        tarefas = carregar_tarefas(caminho=self.arquivo)
        self.assertTrue(sucesso)
        self.assertEqual(tarefas[0]["titulo"], "Lavar carro e moto")
        self.assertEqual(tarefas[0]["status"], "concluida")

    def test_remover_tarefa(self):
        tarefa = adicionar_tarefa({"titulo": "Fazer compras", "descricao": "Lista", "prioridade": "baixa", "prazo": "18/09/2026", "status": "pendente"}, caminho=self.arquivo)
        sucesso = remover_tarefa(tarefa["id"], caminho=self.arquivo)
        tarefas = carregar_tarefas(caminho=self.arquivo)
        self.assertTrue(sucesso)
        self.assertEqual(len(tarefas), 0)

    def test_resumo_tarefas(self):
        adicionar_tarefa({"titulo": "T1", "descricao": "Desc1", "prioridade": "alta", "prazo": "12/09/2026", "status": "pendente"}, caminho=self.arquivo)
        adicionar_tarefa({"titulo": "T2", "descricao": "Desc2", "prioridade": "baixa", "prazo": "13/09/2026", "status": "concluida"}, caminho=self.arquivo)
        resumo = resumo_tarefas(caminho=self.arquivo)
        self.assertEqual(resumo["total"], 2)
        self.assertEqual(resumo["pendentes"], 1)
        self.assertEqual(resumo["concluidas"], 1)

if __name__ == "__main__":
    unittest.main()
