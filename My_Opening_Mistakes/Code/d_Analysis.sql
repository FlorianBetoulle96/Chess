COPY (
    with fens_final as (
        select 
            column0 as fen,
            column1 as b_or_w,
            column2 as move_nb,
            column3 as stck_move,
            round(CAST(column4 AS FLOAT) / 0.2) * 0.2 as stck_eval,
            column5 as my_move,
            round(CAST(column6 AS FLOAT) / 0.2) * 0.2 as my_eval,
            case when column1 = 'w' then (stck_eval - my_eval) else (my_eval - stck_eval) end as diff_eval
        from read_csv_auto('../Files/final_cleaned.csv', delim=',', header=false,null_padding=true)
    )
    , fens_grouped as (
        select 
            fen
            , b_or_w
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
        where 1=1 
            and counter > 1
            and stck_move != my_move
            and diff_eval > 300
        order by counter desc
    )
    select * from worst_moves
) TO '../Files/worst_moves.csv' (HEADER, DELIMITER ',');