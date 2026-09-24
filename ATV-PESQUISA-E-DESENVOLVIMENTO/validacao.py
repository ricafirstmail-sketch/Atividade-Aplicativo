from datetime import datetime

PRIORIDADES_VALIDAS = {"baixa", "media", "alta"}


def normalizar_texto(valor):
    if valor is None:
        return ""
    return str(valor).strip()


def validar_prioridade(prioridade):
    valor = normalizar_texto(prioridade).lower()
    return valor in PRIORIDADES_VALIDAS


def validar_data(data):
    valor = normalizar_texto(data)
    if not valor:
        return False
    try:
        datetime.strptime(valor, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_campos_obrigatorios(dados):
    erros = []
    titulo = normalizar_texto(dados.get("titulo"))
    descricao = normalizar_texto(dados.get("descricao"))
    prioridade = normalizar_texto(dados.get("prioridade"))
    prazo = normalizar_texto(dados.get("prazo"))

    if not titulo:
        erros.append("O campo 'Título' é obrigatório.")
    if not descricao:
        erros.append("O campo 'Descrição' é obrigatório.")
    if not prioridade:
        erros.append("O campo 'Prioridade' é obrigatório.")
    elif not validar_prioridade(prioridade):
        erros.append("A prioridade deve ser 'baixa', 'media' ou 'alta'.")
    if not prazo:
        erros.append("O campo 'Prazo' é obrigatório.")
    elif not validar_data(prazo):
        erros.append("O prazo deve seguir o formato DD/MM/AAAA.")

    return erros


def validar_dados_tarefa(dados):
    return validar_campos_obrigatorios(dados)
