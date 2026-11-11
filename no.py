class no:
    def __init__(self, id, ip, porta, proximo_id, ip_destino, porta_destino, fichas_iniciais):
        
        # Estado do jogador
        self.id = id
        self.fichas = fichas_iniciais

        # Estado da roleta
        self.eh_roleta = False
        self.pote = 0

        # Criacao do socket Datagram
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Abre a porta para escutar mensagens
        self.sock.bind((ip, porta))