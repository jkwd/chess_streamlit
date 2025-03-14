from duckdb import DuckDBPyConnection

from dbt.adapters.duckdb.plugins import BasePlugin
from dbt.adapters.duckdb.utils import TargetConfig

import chess.pgn
from io import StringIO
import chess

from collections import Counter
import re

def pgn_to_fens_udf(pgn) -> list[str]:
    arr = []
    game = chess.pgn.read_game(StringIO(pgn)).game()
    board = game.board()
    
    for move in game.mainline_moves():
        board.push(move)
        fen = board.fen()
        # from_square = move.from_square
        # to_square = move.to_square
        # moved_piece = board.piece_at(to_square).symbol()
        # color_move = board.piece_at(to_square).color
        # x = {
        #     'move_from_to': move.uci(),
        #     'from_square': from_square,
        #     'to_square': to_square,
        #     'moved_piece': moved_piece,
        #     'color_move': 'White' if color_move else 'Black',
        #     'fen': fen
        # }
        # arr.append(x)
        arr.append(fen)

    return arr

def get_checkmate_pieces_udf(fen, player_color, player_result, opponent_result) -> list[str]:
    if not (player_result == 'checkmated' or opponent_result == 'checkmated'):
        return []

    board = chess.Board(fen)

    if not board.is_checkmate():
        return []

    if player_color == 'White':
        if player_result == 'win':
            winning_color = chess.WHITE
            checkmated_color = chess.BLACK
        else:
            winning_color = chess.BLACK
            checkmated_color = chess.WHITE
    else:
        if player_result == 'win':
            winning_color = chess.BLACK
            checkmated_color = chess.WHITE
        else:
            winning_color = chess.WHITE
            checkmated_color = chess.BLACK

    # Get position of Checkmated King
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.KING and piece.color == checkmated_color:
            king_square = square
            break

    # Get possible moves by king
    official_king_moves = board.attacks(king_square)
    attacked_squares = [king_square]
    for square in official_king_moves:
        piece = board.piece_at(square)

        if not piece or piece.color != checkmated_color:
            attacked_squares.append(square)

    # Get attacking pieces
    attacking_pieces = []
    for square in attacked_squares:
        attacker_ids = list(board.attackers(color=winning_color, square=square))
        attacking_pieces.extend(attacker_ids)
    attacking_pieces = set(attacking_pieces)  # dedup the board pieces based on position

    return sorted([chess.piece_name(board.piece_at(attacker).piece_type) for attacker in attacking_pieces])

def get_captured_piece_udf(prev_fen, fen) -> str | None:
    if prev_fen == "":
        return None
    
    prev_fen = prev_fen.split(' ')[0]
    fen = fen.split(' ')[0]
    prev_pieces = re.findall(r'[prnbqRNBQP]', prev_fen)
    current_pieces = re.findall(r'[prnbqRNBQP]', fen)
    
    prev = Counter(prev_pieces)
    curr = Counter(current_pieces)

    # find the difference between the two lists
    diff = prev-curr
    
    captured = list(diff.elements())
    if len(captured) == 0:
        return None
    
    return captured[0]

# The python module that you create must have a class named "Plugin"
# which extends the `dbt.adapters.duckdb.plugins.BasePlugin` class.
class Plugin(BasePlugin):
    def configure_connection(self, conn: DuckDBPyConnection):
        conn.create_function("pgn_to_fens_udf", pgn_to_fens_udf)
        conn.create_function("get_checkmate_pieces_udf", get_checkmate_pieces_udf)
        conn.create_function("get_captured_piece_udf", get_captured_piece_udf, null_handling = 'special')