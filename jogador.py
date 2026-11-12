import socket
import json
import random

class jogador:
    def __init__(self, id, ip, porta, proximo_id, ip_destino, porta_destino, fichas_iniciais):
        
        # Estado do jogador
        self.id = id
        self.fichas = fichas_iniciais

        # Estado da roleta
        self.eh_roleta = False
        self.pote = 0
        self.destino = (ip_destino, porta_destino)

        self.meu_ip = ip
        self.minha_porta = porta
        
        # Criacao do socket Datagram
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Abre a porta para escutar mensagens
        self.sock.bind((ip, porta))

    def iniciar(self):

        if self.id == 1:
            mensagem = {"tipo": 0, "bastao": True}
            dados_bytes = json.dumps(mensagem).encode('utf-8')
            self.sock.sendto(dados_bytes, (self.meu_ip, self.minha_porta))

        while True:
            dados_bytes, endereco_origem = self.sock.recvfrom(1024)
            mensagem = json.loads(dados_bytes.decode('utf-8'))
            self.processar_mensagem(mensagem)
    
    def passar_bastao(self):
        mensagem = {"tipo": 0}
        dados_bytes = json.dumps(mensagem).encode('utf-8')
        self.sock.sendto(dados_bytes, self.destino)

    def processar_mensagem(self, mensagem):
        tipo = mensagem.get("tipo")

        # Mensagem de passagem de bastao
        if tipo == 0:
            print(f"Jogador {self.id} recebeu o bastão e é roleta desta rodada")
            self.eh_roleta = True

            mensagem_apostas = {
                "tipo": 1,
                "apostas": []
            }
            dados = json.dumps(mensagem_apostas).encode('utf-8')
            self.sock.sendto(dados, self.destino)
        
        # Mensagem de apostas
        elif tipo == 1:
            
            if self.eh_roleta:

                print(f"A roleta recebeu as apostas.")
                self.pote = sum(aposta.get("valor", 0) for aposta in apostas)
                print(f"O número sorteado foi: {numero_sorteado}")

                numero_sorteado = random.randint(0, 36)
                par = numero_sorteado % 2 == 0
                cor = "Vermelho" if numero_sorteado in config.VERMELHOS else "Preto"

                premios = {}
                total = 0

                apostas = mensagem.get("apostas", [])
                for aposta in apostas:
                    id_jogador = aposta.get("id_jogador")
                    escolha = aposta.get("escolha")
                    valor = aposta.get("valor")

                    if escolha.isdigit() and int(escolha) == numero_sorteado:
                        premio = valor * 36
                    elif (escolha.lower() == "pares" and par) or
                         (escolha.lower() == "impares" and not par) or
                         (escolha.lower() == "pretos" and cor == "Preto") or
                         (escolha.lower() == "vermelhos" and cor == "Vermelho"):
                        premio = valor * 2

                    if premio > 0:
                        premios[jogador_id] = premio
                        total += premio
                
                self.pote -= total
                # Se o pote ficar negativo, ajusta para zero
                if self.pote < 0:
                    self.pote = 0

                print(f"Total de fichas distribuídas: {total}. Restante de fichas da roleta: {self.pote}")

                mensagem_premios = {
                    "tipo": 2,
                    "premios": premios
                }
                
                dados = json.dumps(mensagem_premios).encode('utf-8')
                self.sock.sendto(dados, self.destino)
            else:
                print(f"--- SUA VEZ DE APOSTAR, JOGADOR {self.id} ---")
                print(f"Saldo atual: {self.fichas} fichas")
                print("Opções de aposta: Número (0-36), Pretos, Vermelhos, Pares, Impares")

                escolha_digitada = input("Digite a sua opção de aposta: ")
                valor_digitado = int(input("Digite o valor da aposta (em fichas): "))

                if valor_digitado > self.fichas:
                    print("O valor digitado é maior que o saldo disponível. A aposta será o saldo total.")
                    valor_digitado = self.fichas

                self.fichas -= valor_digitado

                aposta = {
                    "id_jogador": self.id,
                    "escolha": escolha_digitada, 
                    "valor": valor_digitado
                }

                mensagem["apostas"].append(aposta)
                dados = json.dumps(mensagem).encode('utf-8')
                self.sock.sendto(dados, self.destino)
        
        # Mensagem de resultado da roleta
        elif tipo == 2:

            if self.eh_roleta:
                print(f"Fim da rodada. O próximo jogador será a roleta da vez.")
                self.eh_roleta = False

                self.passar_bastao()
            
            else:
