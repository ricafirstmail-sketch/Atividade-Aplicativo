import json
from pathlib import Path

from validacao import normalizar_texto

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "dados" / "tarefas.json"

def _resolver_arquivo(caminho=None):
    if caminho is None:
        arquivo = ARQUIVO_DADOS
    else:
        arquivo = Path(caminho)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    return arquivo

def _normalizar_tarefa(tarefa):
    if not isinstance(tarefa, dict):
        return {}
    return {
        "id": int(tarefa.get("id", 0) or 0),
        "titulo": normalizar_texto(tarefa.get("titulo")),
        "descricao": normalizar_texto(tarefa.get("descricao")),
        "prioridade": normalizar_texto(tarefa.get("prioridade")).lower(),
        "prazo": normalizar_texto(tarefa.get("prazo")),
        "status": normalizar_texto(tarefa.get("status")).lower() or "pendente",
    }

def carregar_tarefas(caminho=None):
    arquivo = _resolver_arquivo(caminho)
    if not arquivo.exists():
        arquivo.write_text("[]", encoding="utf-8")
    with arquivo.open("r", encoding="utf-8") as handle:
        try:
            dados = json.load(handle)
        except json.JSONDecodeError:
            dados = []
    if not isinstance(dados, list):
        dados = []
    return [_normalizar_tarefa(item) for item in dados]

def salvar_tarefas(tarefas, caminho=None):
    arquivo = _resolver_arquivo(caminho)
    with arquivo.open("w", encoding="utf-8") as handle:
        json.dump(tarefas, handle, ensure_ascii=False, indent=2)

def adicionar_tarefa(tarefa, caminho=None):
    tarefas = carregar_tarefas(caminho)
    nova_tarefa = _normalizar_tarefa(tarefa)
    novo_id = max((item["id"] for item in tarefas), default=0) + 1
    nova_tarefa["id"] = novo_id
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas, caminho)
    return nova_tarefa

def buscar_tarefas(termo, caminho=None):
    consulta = normalizar_texto(termo).lower()
    tarefas = carregar_tarefas(caminho)
    if not consulta:
        return tarefas
    return [
        tarefa
        for tarefa in tarefas
        if consulta in tarefa["titulo"].lower() or consulta in tarefa["descricao"].lower()
    ]

def atualizar_tarefa(tarefa, caminho=None):
    tarefas = carregar_tarefas(caminho)
    tarefa_normalizada = _normalizar_tarefa(tarefa)
    for index, item in enumerate(tarefas):
        if item["id"] == tarefa_normalizada["id"]:
            tarefas[index] = tarefa_normalizada
            salvar_tarefas(tarefas, caminho)
            return True
    return False

def remover_tarefa(tarefa_id, caminho=None):
    tarefas = carregar_tarefas(caminho)
    tarefas_filtradas = [tarefa for tarefa in tarefas if tarefa["id"] != int(tarefa_id)]
    if len(tarefas_filtradas) == len(tarefas):
        return False
    salvar_tarefas(tarefas_filtradas, caminho)
    return True

def resumo_tarefas(caminho=None):
    tarefas = carregar_tarefas(caminho)
    totais = {
        "total": len(tarefas),
        "pendentes": sum(1 for tarefa in tarefas if tarefa["status"] == "pendente"),
        "concluidas": sum(1 for tarefa in tarefas if tarefa["status"] == "concluida"),
    }
    return totais
