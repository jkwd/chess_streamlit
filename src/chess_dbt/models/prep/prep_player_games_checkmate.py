import chess


def get_checkmate_pieces(fen, player_color, player_result, opponent_result):
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


def model(dbt, session):
    df = dbt.ref("prep_player_games").to_df()

    df['checkmate_pieces'] = df[['fen', 'player_color', 'player_result', 'opponent_result']].apply(
        lambda x: get_checkmate_pieces(x.fen,
                                       x.player_color,
                                       x.player_result,
                                       x.opponent_result), axis=1
    )

    return df
