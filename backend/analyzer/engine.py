from io import StringIO
import os
import random
import string
import asyncio
import chess
import chess.engine
import chess.pgn
import json
import redis
import time

# Realiza a conexão com o Redis - Gerenciador de Filas de Análises 
try:
    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    r.ping()
except redis.exceptions.ConnectionError as e:
    exit(1)

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

async def engine_analyse(pgn) -> list:
    evaluation_moves = []

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


def run():
    id_tarefa = ""
    chave_tarefa = ""

    while True:
        try:
            id_tarefa = r.blpop(FILA_ANALISE, timeout=0)[1]
            chave_tarefa = f"{PREFIXO_ANALISE}{id_tarefa}"

            r.hset(chave_tarefa, "status", "Em análise")
            r.hset(chave_tarefa, "iniciado_em", time.time())

            pgn_partida = r.hget(chave_tarefa, "partida")
            resultado_analise = asyncio.run(engine_analyse(pgn_partida))

            r.hset(chave_tarefa, "status", "Concluída")
            r.hset(chave_tarefa, "analise", json.dumps(resultado_analise))
            r.hset(chave_tarefa, "finalizado_em", time.time())
        
        except Exception as error:
            r.hset(chave_tarefa, "status", "Falha")
            r.hset(chave_tarefa, "message", str(error))

if __name__ == "__main__":
    run()
