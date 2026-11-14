import json
import socket

# Cores da saida
RESET = '\033[0m'
VERMELHO_T = '\033[91m'
VERDE_T = '\033[92m'
AMARELO_T = '\033[93m'
AZUL_T = '\033[94m'

# Informacoes das maquinas dos jogadores
MAQUINAS = {
    0: {"ip": "10.254.223.38", "porta": 6268}, # h10
    1: {"ip": "10.254.223.39", "porta": 6269}, # h11
    2: {"ip": "10.254.223.43", "porta": 6270}, # h15
    3: {"ip": "10.254.223.44", "porta": 6271}  # h16
}

PRIMEIRA_ROLETA = 0

# Definicoes do jogo
FICHAS_INICIAIS = 1000
VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

# Tipos de mensagens
BASTAO = 0
APOSTAS = 1
RESULTADOS = 2
SAIR = 3

def enviar_mensagem(mensagem, sock, destino):
    dados_bytes = json.dumps(mensagem).encode('utf-8')
    sock.sendto(dados_bytes, destino)