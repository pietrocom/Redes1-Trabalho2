import sys
import socket
import config
import no

if len(sys.argv) < 2:
    print("Uso: python main.py <id_maquina>")
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

# Inicializa a maquina; cria e abre o socket
jogador = no.no(id, ip_fonte, porta_fonte, proximo_id, ip_destino, porta_destino, config.FICHAS_INICIAIS)

print(f"Iniciando Máquina {id} no IP {ip_fonte}:{porta_fonte}")
print(f"Vou enviar mensagens para a Máquina {proximo_id} em {ip_destino}:{porta_destino}")
