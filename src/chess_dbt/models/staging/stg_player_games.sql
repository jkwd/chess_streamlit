select
    end_time::timestamp as end_time
    , url::string as url
    , pgn::string as pgn
    , time_control::string as time_control
    , rated::boolean as rated
    , accuracies__white::double as accuracies__white
    , accuracies__black::double as accuracies__black
    , tcn::string as tcn
    , uuid::string as game_uuid
    , initial_setup::string as initial_setup
    , fen::string as fen
    , time_class::string as time_class
    , rules::string as rules
    , white__rating::int as white__rating
    , white__result::string as white__result
    , white__aid::string as white__aid
    , white__username::string as white__username
    , white__uuid::string as white__uuid
    , black__rating::int as black__rating
    , black__result::string as black__result
    , black__aid::string as black__aid
    , black__username::string as black__username
    , black__uuid::string as black__uuid
    , _dlt_load_id::double as _dlt_load_id
    , _dlt_id::string as _dlt_id

from {{ source('chess_source', 'players_games') }}
