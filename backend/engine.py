from io import StringIO
import os
import random
import string
import asyncio
import chess
import chess.engine
import chess.pgn
import json

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
    moves_quality = evaluation_quality(evaluation_moves)
    save_analyse(moves_quality)
    return True


def run():
    with open("game.pgn", "r") as game:
        data = game.read()
    asyncio.run(engine_analyse(data))

if __name__ == "__main__":
    run()
