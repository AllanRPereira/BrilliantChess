from io import StringIO
import os
import random
import string
import asyncio
import chess
import chess.engine
import chess.pgn
import json
import time

# Importar redis de forma mais específica para evitar conflitos
try:
    import redis.asyncio as redis
except ImportError:
    import aioredis as redis

# Variável global para controlar se o engine está rodando
engine_running = False

FILA_ANALISE = "analises"
PREFIXO_ANALISE = "analise:"

# ---------------- Sistema de Análise ------------------------------------

def gerar_palavra():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))

def save_analyse(moves_quality : dict):
    if not os.path.exists("partidas_analisadas"):
        os.mkdir("partidas_analisadas")

    with open(f"partidas_analisadas/{gerar_palavra()}.json", "w") as aqv:
        aqv.write(json.dumps(moves_quality))

def evaluation_quality(list_of_moves : list):
    moves_quality = {
        "moves" : []
    }

    options = ["Perfeito!", "Excelente", "Ótimo", "Bom", "Normal", "Impreciso", "Erro", "Erro Grave"]

    for move in list_of_moves:
        moves_quality["moves"].append((move, random.choice(options)))

    return moves_quality

async def engine_analyse(pgn) -> dict:
    evaluation_moves = []

    try:
        data_pgn = StringIO(pgn)
        game = chess.pgn.read_game(data_pgn)
        transport, engine = await chess.engine.popen_uci("engine/stockfish")
        
        board = chess.Board()
        for move in game.mainline_moves():
            info = await engine.analyse(board, chess.engine.Limit(time=0.1))
            evaluation_moves.append((board.san(move), int(info["score"].relative.score()) / 100))
            board.push(move)

        await engine.quit()
        return evaluation_quality(evaluation_moves)
    except Exception as e:
        print(f"Erro na análise do engine: {e}")
        return evaluation_quality([])

async def run():
    global engine_running
    if engine_running:
        return
    
    engine_running = True
    redis_client = None
    
    try:
        # Conecta ao Redis de forma mais robusta
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        id_tarefa = ""
        chave_tarefa = ""

        print("Engine iniciado e aguardando tarefas...")

        while engine_running:
            try:
                # Usa blpop com timeout para não bloquear indefinidamente
                result = await redis_client.blpop(FILA_ANALISE, timeout=1)
                if not result:
                    # Pequena pausa para não consumir muito CPU
                    await asyncio.sleep(0.1)
                    continue
                    
                id_tarefa = result[1]
                chave_tarefa = f"{PREFIXO_ANALISE}{id_tarefa}"

                print(f"Processando tarefa: {id_tarefa}")

                await redis_client.hset(chave_tarefa, "status", "Em análise")
                await redis_client.hset(chave_tarefa, "iniciado_em", time.time())

                pgn_partida = await redis_client.hget(chave_tarefa, "partida")
                resultado_analise = await engine_analyse(pgn_partida)

                await redis_client.hset(chave_tarefa, "status", "Concluída")
                await redis_client.hset(chave_tarefa, "analise", json.dumps(resultado_analise))
                await redis_client.hset(chave_tarefa, "finalizado_em", time.time())
                
                print(f"Tarefa {id_tarefa} concluída com sucesso")
            
            except Exception as error:
                print(f"Erro ao processar tarefa: {error}")
                if chave_tarefa and redis_client:
                    try:
                        await redis_client.hset(chave_tarefa, "status", "Falha")
                        await redis_client.hset(chave_tarefa, "message", str(error))
                    except:
                        pass
                
                # Pequena pausa antes de tentar novamente
                await asyncio.sleep(1)
    
    except Exception as e:
        print(f"Erro fatal no engine: {e}")
    
    finally:
        if redis_client:
            try:
                await redis_client.close()
            except:
                pass
        engine_running = False
        print("Engine parado")

def stop_engine():
    global engine_running
    engine_running = False

def is_engine_running():
    return engine_running

if __name__ == "__main__":
    asyncio.run(run())
