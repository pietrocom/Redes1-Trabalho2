import socket
import json
import random
import utils
import sys

class jogador:
    def __init__(self, id, ip, porta, proximo_id, ip_destino, porta_destino, fichas_iniciais):
        
        # Estado do jogador
        self.id = id
        self.fichas = fichas_iniciais

        # Estado da roleta
        self.eh_roleta = False

        self.destino = (ip_destino, porta_destino)
        self.meu_ip = ip
        self.minha_porta = porta
        
        # Criacao do socket Datagram
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Abre a porta para escutar mensagens
        self.sock.bind((ip, porta))

    def iniciar(self):

        # Primeiro jogador a ser roleta
        if self.id == utils.PRIMEIRA_ROLETA:
            mensagem = {"tipo": utils.BASTAO}
            utils.enviar_mensagem(mensagem, self.sock, (self.meu_ip, self.minha_porta))

        # Loop para receber e processar mensagens
        while True:
            dados_bytes, endereco_origem = self.sock.recvfrom(2048)
            mensagem = json.loads(dados_bytes.decode('utf-8'))
            self.processar_mensagem(mensagem)
    
    def passar_bastao(self):
        self.eh_roleta = False

        mensagem = {"tipo": utils.BASTAO}
        utils.enviar_mensagem(mensagem, self.sock, self.destino)
    
    def ler_opcao(self):
        while True:
            print("    Opções de aposta: Número (0-36), Pretos, Vermelhos, Pares, Impares (Fim para encerrar apostas)")
            opcao = input("    Digite a sua opção de aposta: ").strip()
            
            # Opcao numero
            if opcao.isdigit():
                if int(opcao) > 36:
                    print("    Número inválido! Escolha entre 0 e 36.")
                else:
                    break
            else:
                if opcao.lower() in ["pretos", "vermelhos", "pares", "impares", "fim", "sair"]:
                    break
                else:
                    print("    Opção inválida!")
        
        return opcao

    def ler_valor(self):
        while True:
            valor = input("    Digite o valor da aposta (em fichas): ").strip()
            
            if valor.isdigit():
                valor = int(valor)
                
                if valor > self.fichas:
                    print(f"    Valor maior que o saldo disponível ({self.fichas}).")
                else:
                    break
            else:
                print(f"    Valor inválido! Digite apenas números inteiros positivos.")
        
        return valor
    
    def encerrar_jogo(self):
        print("    Encerrando o jogo...")
        mensagem = {"tipo": utils.SAIR}
        utils.enviar_mensagem(mensagem, self.sock, self.destino)
        sys.exit(0)


    def mandar_aposta(self, mensagem):

        # A roleta envia a mensagem de apostas a ser preenchida
        if self.eh_roleta:
            mensagem = {
                "tipo": utils.APOSTAS,
                "apostas": []
            }

        else:
            print(f"{utils.AZUL_T} --- SUA VEZ DE APOSTAR! SALDO ATUAL: {self.fichas} --- {utils.RESET}")

            # Le as apostas enquanto a entrada for diferente de "fim"
            while True:
                if self.fichas <= 0:
                    print(f"    Você não tem fichas suficientes para apostar nessa rodada")
                    break

                opcao = self.ler_opcao()
                
                if opcao == "fim":
                    print("    Apostas registradas. Passando para o próximo jogador")
                    break
                
                elif opcao == "sair":
                    self.encerrar_jogo()
                    break
                    
                valor = self.ler_valor()

                self.fichas -= valor

                aposta = {
                    "id_jogador": self.id,
                    "escolha": opcao, 
                    "valor": valor
                }

                # Adiciona a aposta na lista da mensagem
                mensagem["apostas"].append(aposta)

        # Envia a mensagem suas apostas e anteriores para o proximo jogador
        utils.enviar_mensagem(mensagem, self.sock, self.destino)
    
    def receber_premio(self, mensagem):
        premios = mensagem.get("premios", {})
        fichas_ganhas = premios.get(str(self.id), 0)

        if fichas_ganhas > 0:
            self.fichas += fichas_ganhas
            print(f"{utils.VERDE_T}    Você acertou a aposta! Fichas recebidas: {fichas_ganhas}. Fichas totais: {self.fichas}")
        
        else: 
            print(f"{utils.VERMELHO_T}    Você não acertou a aposta. Nenhuma ficha recebida")
        
        utils.enviar_mensagem(mensagem, self.sock, self.destino)

    def resultado(self, mensagem):

        # Adiciona as apostas as fichas da roleta
        apostas = mensagem.get("apostas", [])
        self.fichas += sum(aposta.get("valor", 0) for aposta in apostas)

        # Sorteia o numero da roleta
        numero_sorteado = random.randint(0, 36)
        print(f"    O número sorteado foi: {numero_sorteado}")

        # Categoriza o numero sorteado
        par = numero_sorteado % 2 == 0
        cor = "Vermelho" if numero_sorteado in utils.VERMELHOS else "Preto"

        premios = {}
        total = 0

        # Calcula os premios de cada aposta
        apostas = mensagem.get("apostas", [])
        for aposta in apostas:
            id_jogador = aposta.get("id_jogador")
            escolha = aposta.get("escolha").lower()
            valor = aposta.get("valor")
            premio = 0

            if escolha.isdigit() and int(escolha) == numero_sorteado:
                premio = valor * 36
            elif ((escolha == "pares" and par) or
                    (escolha == "impares" and not par) or
                    (escolha == "pretos" and cor == "Preto") or
                    (escolha == "vermelhos" and cor == "Vermelho")):
                premio = valor * 2

            # Soma ao valor existente ou a zero caso ainda nao exista
            premios[id_jogador] = premios.get(id_jogador, 0) + premio
            total += premio
        
        self.fichas -= total
        # Se as fichas ficar negativo, ajusta para zero
        if self.fichas < 0:
            self.fichas = 0

        print(f"    Total de fichas distribuídas: {total}. Fichas restantes na roleta: {self.fichas}")

        mensagem_premios = {
            "tipo": utils.RESULTADOS,
            "premios": premios
        }

        return mensagem_premios

    def processar_mensagem(self, mensagem):
        tipo = mensagem.get("tipo")

        # Mensagem de passagem de bastao
        if tipo == utils.BASTAO:
            print(f"{utils.AMARELO_T} --- VOCÊ É A ROLETA (SERVIDOR) DA RODADA ---{utils.RESET}")

            self.eh_roleta = True
            self.mandar_aposta(mensagem)
        
        # Mensagem de apostas
        elif tipo == utils.APOSTAS:
            
            # Se for a roleta, calcula o resultado e envia a mensagem de resultados
            if self.eh_roleta:
                print(f"    A roleta recebeu as apostas.")

                mensagem_premios = self.resultado(mensagem)
                
                utils.enviar_mensagem(mensagem_premios, self.sock, self.destino)

            # Senao, adiciona suas apostas a mensagem e envia para o proximo jogador
            else:
                self.mandar_aposta(mensagem)
        
        # Mensagem de resultado da roleta
        elif tipo == utils.RESULTADOS:

            # Se for a roleta, o resultado ja passou por todos os jogadores
            if self.eh_roleta:
                print(f"    Fim da rodada. O próximo jogador será a roleta da vez.")

                self.passar_bastao()
            
            # Recebe o premio calculado pela roleta
            else:
                self.receber_premio(mensagem)
        
        elif tipo == utils.SAIR:
            self.encerrar_jogo()
