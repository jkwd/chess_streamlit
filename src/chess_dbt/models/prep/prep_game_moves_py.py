import chess.pgn
from io import StringIO
import chess
import re
import pandas as pd
import numpy as np
from collections import Counter

def get_is_backrank_sparse(fen):
    black_backrank = fen.split(' ')[0].split('/')[0]
    black_major_minor = len(re.findall(r'[rnbq]', black_backrank))
    
    white_backrank = fen.split(' ')[0].split('/')[-1]
    white_major_minor = len(re.findall(r'[RNBQ]', white_backrank))
    
    return black_major_minor < 4 or white_major_minor < 4
    
def get_forked_pieces(fen, to_square):
    forked_pieces = []

    board = chess.Board(fen)
    piece = board.piece_at(to_square)
    piece_color = piece.color
    
    piece_attack_squares = board.attacks(to_square)
    for square in piece_attack_squares:
        attacked_piece = board.piece_at(square)
        if attacked_piece is not None and attacked_piece.color != piece_color and attacked_piece.piece_type != chess.PAWN:
            forked_pieces.append(attacked_piece.symbol())
    
    if len(forked_pieces) < 2:
        return []
    return forked_pieces

def get_captured_piece(prev_fen, fen):
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
    

def model(dbt, session):
    df = dbt.ref("prep_player_games").to_df()

    # Extract the move and clock from the pgn into a list and explode it
    # 1 row represents 1 move now
    df['move_unnest'] = df['pgn_move_extract']
    df['clock_unnest'] = df['pgn_clock_extract']
    df = df.explode(['move_unnest','clock_unnest']).reset_index(drop=True)

    # Game move index
    df['game_move_index'] = df.groupby(['game_uuid']).cumcount() + 1
    df['id'] = df['game_uuid'].astype(str) + '_' + df['game_move_index'].astype(str)

    # Cumulative join the moves to get the pgn up to that move
    df['pgn_cum_move'] = df[['pgn_move_extract', 'game_move_index']].apply(lambda x: x['pgn_move_extract'][:x['game_move_index']], axis=1)
    df['pgn_cum_move'] = df['pgn_cum_move'].apply(lambda x: ' '.join(x))

    # Get board details
    df['fen'] = df['pgn_cum_move'].apply(lambda x: chess.pgn.read_game(StringIO(x)).game().end().board().fen())
    df['prev_fen'] = df.groupby(['game_uuid'])['fen'].shift(1).fillna("")

    df['major_minor_cnt'] = df['fen'].str.split(' ').str[0].apply(lambda x: len(re.findall(r'[rnbqRNBQ]', x)))

    # Get move details
    df['color_move_index_raw'] = df['move_unnest'].str.split(' ').str[0]
    df['color_move_index'] = df['color_move_index_raw'].apply(lambda x: int(re.sub(r'\.', '', x)))
    df['color_move'] = df['color_move_index_raw'].apply(lambda x: 'Black' if '...' in x else 'White')

    df['game_move'] = df['move_unnest'].str.split(' ').str[1]
    df['move_from_to'] = df['pgn_cum_move'].apply(lambda x: chess.pgn.read_game(StringIO(x)).game().end().move)
    df['from_square'] = df['move_from_to'].apply(lambda x: x.from_square)
    df['to_square'] = df['move_from_to'].apply(lambda x: x.to_square)
    df['moved_piece'] = df[['fen', 'to_square']].apply(lambda x: chess.Board(x['fen']).piece_at(x['to_square']).symbol(), axis=1)
    df['captured_piece'] = df[['prev_fen', 'fen']].apply(lambda x: get_captured_piece(x['prev_fen'], x['fen']), axis=1)

    # Get clock details
    df['clock_interval_post_move'] = df['clock_unnest'].str.split(' ').str[1].apply(lambda x: pd.to_timedelta(x.replace(']}', '')).total_seconds())
    df['clock_interval_move'] = df['clock_interval_post_move'] - df['time_control_add_seconds']
    df['prev_clock_interval'] = df.groupby(['game_uuid','color_move'])['clock_interval_post_move'].shift(1).fillna(df['time_control_base'])
    df['move_time_seconds'] = df['prev_clock_interval'] - df['clock_interval_move']

    # Handle daily games
    df['prev_clock_interval'] = np.where(df['time_class'] == 'daily', 0, df['prev_clock_interval'])
    df['clock_interval_move'] = np.where(df['time_class'] == 'daily', 0, df['clock_interval_move'])
    df['clock_interval_post_move'] = np.where(df['time_class'] == 'daily', 0, df['clock_interval_post_move'])
    df['move_time_seconds'] = np.where(df['time_class'] == 'daily', 0, df['move_time_seconds'])

    # Board details
    df['major_minor_cnt'] = df['fen'].str.split(' ').str[0].apply(lambda x: len(re.findall(r'[rnbqRNBQ]', x)))
    df['is_backrank_sparse'] = df['fen'].str.split(' ').str[0].apply(lambda x: get_is_backrank_sparse(x))

    df['is_midgame'] = np.where(
        (df['major_minor_cnt'] <= 10) | df['is_backrank_sparse'],
        True,
        False
    )
    df['is_endgame'] = np.where(
        df['is_midgame'] & (df['major_minor_cnt'] <= 6),
        True,
        False
    )
    df['game_phase'] = np.where(
        df['is_endgame'],'Endgame',
        np.where(df['is_midgame'],'Midgame','Opening')
    )

    df['forked_pieces'] = df[['fen', 'to_square']].apply(lambda x: get_forked_pieces(x['fen'], x['to_square']), axis=1)

    df = df[['id',
            'time_class', 
            'time_control_base', 
            'time_control_add_seconds', 
            'game_uuid',
            'game_move_index',
            'color_move',
            'color_move_index',
            'game_move',
            'pgn_cum_move',
            'fen',
            'from_square',
            'to_square',
            'moved_piece',
            'forked_pieces',
            'captured_piece',
            'major_minor_cnt',
            'is_backrank_sparse',
            'is_midgame',
            'is_endgame',
            'game_phase',
            'prev_clock_interval',
            'clock_interval_move',
            'clock_interval_post_move',
            'move_time_seconds']]
    
    return df