# Relatório Trabalho 2: Rede em Anel - Redes 2
**Autores:** Camila Shibata (GRR20245211) e Pietro Comin (GRR20241955)

## 1. Visão Geral
O trabalho consiste em um jogo de roleta em uma **Rede em Anel**. A comunicação é realizada em direção única, onde cada máquina (jogador) conhece apenas seu vizinho direto.

## 2. Estrutura das Mensagens
Todas as mensagens enviadas na rede são objetos JSON contendo a chave `"tipo"` (inteiro), que direciona o fluxo de execução para cada caso.

### Tipo 0: Passagem de Bastão (`BASTAO`)
O jogador que recebe essa mensagem assume o papel de roleta (Servidor) para a rodada atual. A roleta então envia a mensagem para coletar as apostas.
- **Estrutura:** `{"tipo": 0}`

### Tipo 1: Coleta de Apostas (`APOSTAS`)
Viaja pelo anel coletando as apostas de cada nó em formato de lista até retornar à Roleta. Um jogador anexa suas apostas e passa a mensagem para o próximo. A Roleta sorteia um número, lê as apostas e calcula os prêmios.
* **Estrutura:**
  ```json
  {
    "tipo": 1,
    "apostas": [
      {
        "id_jogador": 2,
        "escolha": "vermelhos",
        "valor": 50
      },
      {
        "id_jogador": 2,
        "escolha": "17",
        "valor": 10
      }
    ]
  }
  ```

### Tipo 2: Distribuição de Resultados (`RESULTADOS`)
Disparada pela roleta após a coleta de apostas. Contém o número de fichas que cada jogador ganhou. Cada jogador recebe as fichas ganhas e passa a mensagem para o próximo. Ao retornar à roleta, o bastão é passado e o próximo jogador passa a ser roleta.
* **Estrutura:**
  ```json
  {
    "tipo": 2,
    "premios": {
      "1": 300,
      "2": 140,
      "3": 400,
      "4": 220
    }
  }
  ```

## 3. Fluxo de Execução
- O jogador `x` recebe o bastão e portanto é a roleta da rodada. A roleta envia a mensagem de `APOSTAS` vazia
- Os demais jogadores adicionam suas apostas à mensagem
- A roleta recebe as apostas, realiza o sorteio, calcula os prêmios e envia a mensagem de `RESULTADOS`
- Os demais jogadores recebem as fichas ganhas e passam a mensagem
- A mensagem retorna à roleta, então ela passa o bastão para transferir a roleta