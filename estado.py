# estado.py
__all__ = ["respostas", "setup_cache", "tela_atual"]

# falta criar um ID de pesquisa persistente e aditivo
# sugestao foi usar data e hora do inicio da pesquisa

# guarda respostas da entrevista atual
respostas = {}

# guarda o último setup preenchido
setup_cache = {
    "S_1": "", # Device_ID (Automático)
    "S_2": "", # Data (Automático)
    "S_3": "", # Hora (Automático)
    "S_4": "", # Nome pesquisador
    "S_5": None, # Local Posto
    "S_6": "Interior", # Sentido (Padrão)
    "S_7": "Sol", # Clima (Padrão)
}

# controle de navegação
tela_atual = "t3" #"setup"
