select game_uuid
from {{ ref('prep_player_games_checkmate') }}
where
    player_result <> 'checkmated'
    and opponent_result <> 'checkmated'
    and len(checkmate_pieces) > 0
