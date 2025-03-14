{% docs url %}
The url of the game in chess.com
{% enddocs %}

{% docs pgn %}
PGN (short for Portable Game Notation) is the standard format for recording a game in a text file that is processible by computers. The PGN also stores other information like the names of the players, the place where the game was played, the time control, the players' ratings, the game's result, and so on. Therefore, you can think of it as a chess score sheet that computers can read.
{% enddocs %}

{% docs time_control %}
The game time in seconds
{% enddocs %}

{% docs end_time %}
The timestamp in which the game ended
{% enddocs %}

{% docs rated %}
Flag to indicate if the game is rated which impacts the elo rating
{% enddocs %}

{% docs accuracies__white %}
The overall game accuracy for white calculated by chess.com
{% enddocs %}

{% docs accuracies__black %}
The overall game accuracy for black calculated by chess.com
{% enddocs %}

{% docs game_uuid %}
The chess game unique id
{% enddocs %}

{% docs initial_setup %}
The initial chess board pieces setup
{% enddocs %}

{% docs fen %}
The position of the pieces
{% enddocs %}

{% docs time_class %}
Ratings-group speed of the game. Possible values are: "daily", "rapid", "blitz", "bullet".
{% enddocs %}

{% docs rules %}
To indicate chess-variant play. Possible values are: "chess", "chess960", "bughouse", "kingofthehill", "threecheck", "crazyhouse"
{% enddocs %}

{% docs white__rating %}
The player white's rating after the game finished
{% enddocs %}

{% docs white__result %}
The result of player white. E.g. win/checkmated/etc.
{% enddocs %}

{% docs white__aid %}
API url to player white.
{% enddocs %}

{% docs white__username %}
Username of player white.
{% enddocs %}

{% docs white__uuid %}
Unique identifier of player white
{% enddocs %}

{% docs black__rating %}
The player black's rating after the game finished
{% enddocs %}

{% docs black__result %}
The result of player black. E.g. win/checkmated/etc.
{% enddocs %}

{% docs black__aid %}
API url to player black.
{% enddocs %}

{% docs black__username %}
Username of player black.
{% enddocs %}

{% docs black__uuid %}
Unique identifier of player black
{% enddocs %}

{% docs time_control_base %}
In chess time control there is a base time and an increment time. For example, 15|10 indicates a base of 15 mins and increment of 10 seconds per move. This column captures the base time in seconds.
{% enddocs %}


{% docs time_control_add_seconds %}
In chess time control there is a base time and an increment time. For example, 15|10 indicates a base of 15 mins and increment of 10 seconds per move. This column captures the incremental time in seconds.
{% enddocs %}

{% docs pgn_header %}
PGN details without the move set
{% enddocs %}

{% docs pgn_moves %}
The string of the move sequence in the entire PGN. This contains the move and the system clock timing of the move
{% enddocs %}

{% docs pgn_move_extract %}
The list of moves extracted from pgn_moves
{% enddocs %}

{% docs pgn_clock_extract %}
The list of timings of each move from pgn_moves
{% enddocs %}

{% docs pgn_move_extract_string %}
The sequence of pgn move extract in string format
{% enddocs %}

{% docs game_analysis_url %}
The link to an open source (Lichess) analysis of the game
{% enddocs %}

{% docs eco %}
Encyclopaedia of Chess Openings
{% enddocs %}

{% docs eco_url %}
Chess.com link to the given Encyclopaedia of Chess Openings
{% enddocs %}

{% docs eco_name %}
Name of the Chess Openings played in the game
{% enddocs %}

{% docs player_color %}
Color of the player of interest in the game
{% enddocs %}

{% docs player_rating %}
Rating of the player of interest in the game upon completion
{% enddocs %}

{% docs player_result %}
Result of the player of interest in the game
{% enddocs %}

{% docs opponent_rating %}
Rating of the opponent of interest in the game upon completion
{% enddocs %}

{% docs opponent_result %}
Result of the opponent of interest in the game
{% enddocs %}

{% docs is_stronger_opponent %}
Flag to indicate if the opponent is stronger
{% enddocs %}

{% docs player_wdl %}
Indicate if the player win/lost/draw the game
{% enddocs %}

{% docs player_wdl_reason %}
Explains the reason of the player's result
{% enddocs %}

{% docs game_start_date %}
Date in which the game started
{% enddocs %}

{% docs game_start_time %}
Time in which the game started
{% enddocs %}

{% docs game_start_timestamp %}
Timestamp in which the game started
{% enddocs %}

{% docs game_end_timestamp %}
Timestamp in which the game ended
{% enddocs %}

{% docs time_played_interval %}
Duration of the game played
{% enddocs %}

{% docs time_played_seconds %}
Duration of the game played in seconds
{% enddocs %}

{% docs checkmate_pieces %}
List of pieces used to checkmate
{% enddocs %}

{% docs game_moves_id %}
ID of the game move, a combination of game uuid and the game move index.
{% enddocs %}

{% docs game_move_index %}
The move index of a given game
{% enddocs %}

{% docs color_move %}
The player color (white/black) that made the move
{% enddocs %}

{% docs color_move_index %}
The index that the player color (white/black) that made the move
{% enddocs %}

{% docs game_move %}
The move that is made
{% enddocs %}

{% docs pgn_cum_move %}
The pgn moves until this game move index
{% enddocs %}

{% docs from_square %}
The board index the move started from
{% enddocs %}

{% docs to_square %}
The board index the piece was moved to
{% enddocs %}

{% docs moved_piece %}
The piece that was moved. Uppercase represents White
{% enddocs %}

{% docs forked_pieces %}
The list of pieces being attacked from this move
{% enddocs %}

{% docs captured_piece %}
The piece that was captured from the move
{% enddocs %}

{% docs major_minor_cnt %}
The number of major and minor pieces on the board after the move is made.
{% enddocs %}

{% docs black_major_minor %}
The number of major and minor pieces on the board after the move is made for black
{% enddocs %}

{% docs white_major_minor %}
The number of major and minor pieces on the board after the move is made for white
{% enddocs %}

{% docs is_backrank_sparse %}
Flag to indicate if the backrank is sparse
{% enddocs %}

{% docs is_midgame %}
Flag to indicate if the game has reached middle game
{% enddocs %}

{% docs is_endgame %}
Flag to indicate if the game has reached the end game
{% enddocs %}

{% docs game_phase %}
Phase the game is at after the move is made
{% enddocs %}

{% docs prev_clock_interval %}
The clock time indicated before the move was made
{% enddocs %}

{% docs clock_interval_move %}
The clock time indicated after the move is made before the increment
{% enddocs %}

{% docs clock_interval_post_move %}
The clock time indicated after the move is made after the increment is added
{% enddocs %}

{% docs move_time_seconds %}
The time taken for the move to be made
{% enddocs %}

{% docs white_total_move_time %}
The time taken for white to move in the game
{% enddocs %}

{% docs white_num_moves %}
The moves taken for white to move in the game
{% enddocs %}

{% docs black_total_move_time %}
The time taken for black to move in the game
{% enddocs %}

{% docs black_num_moves %}
The moves taken for black to move in the game
{% enddocs %}

{% docs player_total_move_time %}
The time taken for player to move in the game
{% enddocs %}

{% docs player_num_moves %}
The moves taken for player to move in the game
{% enddocs %}

{% docs opponent_total_move_time %}
The time taken for opponent to move in the game
{% enddocs %}

{% docs opponent_num_moves %}
The moves taken for opponent to move in the game
{% enddocs %}

{% docs ended_game_phase %}
Phase in which the game ended
{% enddocs %}

{% docs game_mode %}
The time class and the time control
{% enddocs %}

