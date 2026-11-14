import sys
import socket
import utils
import jogador

# Argumento de execucao: id da maquina
if len(sys.argv) < 2:
    print("Uso: python3 main.py <id_maquina>")
    sys.exit()

id = int(sys.argv[1])

# Define para qual maquina enviara as mensagens (vizinha no anel)
proximo_id = (id + 1) % 4

ip_fonte = utils.MAQUINAS[id]["ip"]
porta_fonte = utils.MAQUINAS[id]["porta"]
ip_destino = utils.MAQUINAS[proximo_id]["ip"]
porta_destino = utils.MAQUINAS[proximo_id]["porta"]

# Inicializa o jogador; cria e abre o socket
jogador = jogador.jogador(id, ip_fonte, porta_fonte, proximo_id, ip_destino, porta_destino, utils.FICHAS_INICIAIS)

print(f" JOGADOR {id} IP {ip_fonte}:{porta_fonte}")

# Inicia a execucao (envia primeira mensagem ou comeca a processar mensagens)
jogador.iniciar()
