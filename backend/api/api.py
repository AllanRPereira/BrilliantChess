from fastapi import FastAPI
import redis

# Realiza a conexão com o Redis - Gerenciador de Filas de Análises 
try:
    r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)
    r.ping()
except redis.exceptions.ConnectionError as e:
    exit(1)

FILA_ANALISE = "analises"
PREFIXO_ANALISE = "analise:"

app = FastAPI()

@app.get("/")
def index():
    return {"Message" : "Hello World"}

@app.get("/get-all")
def get_all():
    tarefas = r.lrange(FILA_ANALISE, 0, -1)
    if not tarefas:
        return {"Msg" : tarefas}

    data = []
    for tarefa in tarefas:
        data.append(tarefa.get("id"))
    return {"Msg" : data}