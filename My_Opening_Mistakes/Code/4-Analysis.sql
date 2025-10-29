with fens_final as (
    select 
        c1 as fen,
        c2 as b_or_w,
        c3 as move_nb,
        c4 as stck_move,
        round(c5 / 0.2) * 0.2 as stck_eval,
        c6 as my_move,
        round(c7 / 0.2) * 0.2 as my_eval,
        case when c2 = 'w' then (stck_eval - my_eval) else (my_eval - stck_eval) end as diff_eval
    from read_csv_auto('../Files/final_cleaned.csv');
)
, fens_grouped as (
    select 
        fen
        , b_or_w
        -- , move_nb
        , any_value(stck_move) as stck_move
        , avg(stck_eval) as stck_eval
        , any_value(my_move) as my_move
        , avg(my_eval) as my_eval
        , avg(diff_eval) as diff_eval
        , count(*) as counter
    from fens_final
    group by fen, b_or_w
)
, worst_moves as (
    select fen, b_or_w
    , stck_move
    , round(stck_eval,1) as stck_eval
    , my_move
    , round(my_eval,1) as my_eval
    , round(diff_eval,1) as diff_eval
    , counter  
    from fens_grouped
    where counter > 2
        and stck_move != my_move
        and diff_eval > 0.7
    order by counter desc
)
select * from worst_moves;

COPY (
    SELECT * FROM worst_moves
) TO '../Files/worst_moves.csv' (HEADER, DELIMITER ',');