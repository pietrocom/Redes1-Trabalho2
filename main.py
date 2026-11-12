import sys
import socket
import config
import jogador

if len(sys.argv) < 2:
    print("Uso: python3 main.py <id_maquina>")
    sys.exit()

id = int(sys.argv[1])

if id == 4:
    proximo_id = 1
else:
    proximo_id = id + 1

ip_fonte = config.MAQUINAS[id]["ip"]
porta_fonte = config.MAQUINAS[id]["porta"]

ip_destino = config.MAQUINAS[proximo_id]["ip"]
porta_destino = config.MAQUINAS[proximo_id]["porta"]

# Inicializa o jogador; cria e abre o socket
jogador = jogador.jogador(id, ip_fonte, porta_fonte, proximo_id, ip_destino, porta_destino, config.FICHAS_INICIAIS)
