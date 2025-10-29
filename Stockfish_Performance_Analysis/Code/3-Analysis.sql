with base as (
    select *
    from ../Files/perf_results_cleaned.csv
)
, stats as (
    select round(avg(elo_estim/100),0)*100 as elo_est
        , round(avg(abs(score_avg)), 0) as score_avg 
        , round(avg(pct_same_move), 2) as pct_same_move
        , round(avg(diff_avg),0) as diff_avg
        , round(avg(diff_max),0) as diff_max
    from base
    group by time_limit
    order by time_limit
)
-- select * from base
select * from stats
;

COPY (
    SELECT * FROM worst_moves
) TO '../Files/stockfish_analysis.csv' (HEADER, DELIMITER ',');