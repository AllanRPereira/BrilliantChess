import redis
import uuid 
import time

# Realiza a conexão com o Redis - Gerenciador de Filas de Análises 
try:
    r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)
    r.ping()
    print("Conexão com Redis foi realizada!")
except redis.exceptions.ConnectionError as e:
    exit(1)

FILA_ANALISE = "analises"
PREFIXO_ANALISE = "analise:"

# --- Geração de Requisições  -------
def adicionar_analise():
    for _ in range(10):
        with open("example.pgn", "r") as jogo:
            content = jogo.read()

        id_analise = str(uuid.uuid4())
        chave_analise = f"{PREFIXO_ANALISE}{id_analise}"
        r.hset(chave_analise, mapping={
            "id" : id_analise,  
            "partida" : content,
            "status" : "Em andamento",
            "criado em" : time.time()
        })
        r.rpush(FILA_ANALISE, id_analise)
        print("Análise encaminhada para a fila")

if __name__ == "__main__":
    adicionar_analise()