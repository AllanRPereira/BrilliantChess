from fastapi import FastAPI
import asyncio
from engine import run, stop_engine, is_engine_running 

# Importar redis de forma mais específica para evitar conflitos
try:
    import redis.asyncio as redis
    r = redis.from_url("redis://localhost:6379", decode_responses=True)
except ImportError:
    import aioredis as redis
    r = redis.from_url("redis://localhost:6379", decode_responses=True)

# Teste de conexão
async def test_redis_connection():
    try:
        await r.ping()
        print("Conexão com Redis foi realizada!")
        return True
    except Exception as e:
        print(f"Erro na conexão com Redis: {e}")
        return False

FILA_ANALISE = "analises"
PREFIXO_ANALISE = "analise:"

app = FastAPI()

# Task para rodar o engine em background
engine_task = None

@app.get("/")
def index():
    return {"Message" : "Hello World"}

@app.get("/start-engine")
async def start_engine():
    global engine_task
    
    if is_engine_running():
        return {"message": "Engine já está rodando"}
    
    # Inicia o engine em background
    engine_task = asyncio.create_task(run())
    
    return {"message": "Engine iniciado com sucesso"}

@app.get("/stop-engine")
async def stop_engine_endpoint():
    global engine_task
    
    if not is_engine_running():
        return {"message": "Engine não está rodando"}
    
    # Para o engine
    stop_engine()
    
    # Aguarda a task terminar
    if engine_task:
        try:
            await asyncio.wait_for(engine_task, timeout=5.0)
        except asyncio.TimeoutError:
            engine_task.cancel()
        engine_task = None
    
    return {"message": "Engine parado com sucesso"}

@app.get("/engine-status")
def engine_status():
    return {"running": is_engine_running()}

@app.get("/get-all")
async def get_all():
    try:
        tarefas = await r.lrange(FILA_ANALISE, 0, -1)
        if not tarefas:
            return {"Msg": []}

        data = []
        for id_tarefa in tarefas:
            chave_tarefa = f"{PREFIXO_ANALISE}{id_tarefa}"
            tarefa_data = await r.hgetall(chave_tarefa)
            data.append(tarefa_data)
        return {"Msg": data}
    except Exception as e:
        return {"error": f"Erro ao buscar dados: {str(e)}"}

@app.on_event("startup")
async def startup_event():
    """Testa conexão com Redis e opcionalmente inicia o engine"""
    await test_redis_connection()

    global engine_task
    if not is_engine_running():
        engine_task = asyncio.create_task(run())
        print("Engine iniciado automaticamente!")

@app.on_event("shutdown")
async def shutdown_event():
    """Para o engine quando a API for encerrada"""
    global engine_task
    if is_engine_running():
        stop_engine()
        if engine_task:
            try:
                await asyncio.wait_for(engine_task, timeout=5.0)
            except asyncio.TimeoutError:
                engine_task.cancel()
        print("Engine parado!")
    try:
        await r.close()
    except:
        pass