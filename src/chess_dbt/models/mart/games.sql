{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        unique_key='game_uuid'
    )
}}

with game_moves as (
    select
        game_uuid
        , game_move_index
        , game_phase

        , color_move
        , move_time_seconds
    from {{ ref('prep_game_moves') }}

    where player_username = '{{ var("username") }}'
)

, game_moves_pivot as (
    pivot game_moves
    on color_move
    using sum(move_time_seconds) as total_move_time, count(*) as num_moves
    group by game_uuid
)

, ended_game_phase as (
    select
        game_uuid
        , max_by(game_phase, game_move_index) as ended_game_phase
    from game_moves
    group by game_uuid
)

, player_games as (
    select *
    from {{ ref('prep_player_games') }}
)

, joined as (
    select
        pg.*
        , gm.white_total_move_time
        , gm.white_num_moves
        , gm.black_total_move_time
        , gm.black_num_moves
        , egp.ended_game_phase
    from player_games as pg

    left join game_moves_pivot as gm
        on pg.game_uuid = gm.game_uuid

    left join ended_game_phase as egp
        on pg.game_uuid = egp.game_uuid
)

, final as (
    select
        *

        -- PLAYER DETAILS
        , if(
            player_color = 'White', white_total_move_time, black_total_move_time
        ) as player_total_move_time
        , if(player_color = 'White', white_num_moves, black_num_moves)
            as player_num_moves

        -- OPPONENT DETAILS
        , if(
            player_color = 'White', black_total_move_time, white_total_move_time
        ) as opponent_total_move_time
        , if(player_color = 'White', black_num_moves, white_num_moves)
            as opponent_num_moves

    from joined
)

select
    -- ID
    game_uuid

    -- GAME
    , url
    , rated
    , rules
    , time_class
    , game_mode
    , game_analysis_url

    -- TIME
    , time_control
    , time_control_base
    , time_control_add_seconds
    , time_played_seconds
    , game_start_date
    , game_start_time
    , game_start_timestamp
    , game_end_timestamp

    -- WHITE-BLACK
    , white__uuid
    , white__username
    , white__aid
    , white__rating
    , white__result
    , white_total_move_time
    , white_num_moves

    , black__uuid
    , black__username
    , black__aid
    , black__rating
    , black__result
    , black_total_move_time
    , black_num_moves

    -- PLAYER-OPPONENT
    , player_username
    , player_color
    , player_rating
    , player_result
    , player_total_move_time
    , player_num_moves
    , opponent_rating
    , opponent_result
    , opponent_total_move_time
    , opponent_num_moves
    , is_stronger_opponent
    , player_wdl
    , player_wdl_reason
    , initial_setup

    -- BOARD
    , fen
    , pgn
    , pgn_moves
    , pgn_move_extract
    , pgn_clock_extract
    , eco
    , eco_url
    , eco_name
    , checkmate_pieces
    , ended_game_phase
    , tcn

    -- MISC
    , accuracies__white
    , accuracies__black
    , floor(opponent_rating / 100) * 100 as opponent_rating_bin

from final
