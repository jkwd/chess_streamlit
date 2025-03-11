with player_games as (
    select *
    from {{ ref('stg_player_games') }}
)

, final as (
    select
        *

        -- Time control details
        , case
            when time_class = 'daily' then split(time_control, '/')[2]
            else split(time_control, '+')[1]
        end::int as time_control_base
        , case
            when time_class = 'daily' then '0'
            else coalesce(split(time_control, '+')[2], '0')
        end::int as time_control_add_seconds
        , case
            when
                time_class = 'daily'
                then
                    'daily '
                    || (time_control_base / 3600 / 24)::int::varchar
                    || ' days'
            else time_class || ' ' || time_control
        end as game_mode

        -- PLAYER details
        , if(lower(white__username) = '{{ var("username") }}', 'White', 'Black')
            as player_color
        , if(player_color = 'White', white__rating, black__rating)
            as player_rating
        , if(player_color = 'White', white__result, black__result)
            as player_result

        -- OPPONENT DETAILS
        , if(player_color = 'White', black__rating, white__rating)
            as opponent_rating
        , if(player_color = 'White', black__result, white__result)
            as opponent_result

        -- PLAYER-OPPONENT DETAILS
        , opponent_rating > player_rating as is_stronger_opponent
        , case
            when player_result = 'win' then 'win'
            when opponent_result = 'win' then 'lose'
            when player_result <> 'win' and opponent_result <> 'win' then 'draw'
            else 'unknown'
        end as player_wdl
        , if(player_result = 'win', opponent_result, player_result)
            as player_wdl_reason

        -- PGN details
        , regexp_split_to_array(pgn, '\n\n')[2] as pgn_moves
        , regexp_extract_all(pgn_moves, '\d+\.+ [\S]+') as pgn_move_extract
        , regexp_extract_all(pgn_moves, '{\[%clk \S+\]}') as pgn_clock_extract
        , list_reduce(pgn_move_extract, (s, x) -> s || ' ' || x) as pgn_move_extract_string
        , 'https://lichess.org/analysis/pgn/'
        || replace(replace(pgn_move_extract_string, ' ', '%20'), '#', '')
        || '?color='
        || lower(player_color) as game_analysis_url

        -- PGN ECO details
        , regexp_extract(pgn, '(ECO )"(.*)"', 2) as eco
        , regexp_extract(pgn, '(ECOUrl )"(.*)"', 2) as eco_url
        , replace(eco_url, 'https://www.chess.com/openings/', '') as eco_name

        -- GAME TIME DETAILS
        , replace(regexp_extract(pgn, '(UTCDate )"(.*)"', 2), '.', '-')::date
            as game_start_date
        , regexp_extract(pgn, '(StartTime )"(.*)"', 2) as game_start_time
        , concat(game_start_date, ' ', game_start_time)::timestamp
            as game_start_timestamp
        , end_time::timestamp as game_end_timestamp
        , age(game_end_timestamp, game_start_timestamp) as time_played_interval
        , epoch(time_played_interval) as time_played_seconds
    from player_games
)

select *
from final
