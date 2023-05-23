WITH cte_corr_sentiment AS (

    SELECT round_time_1m("Creationtime") hour_beginning, AVG("Sentiment") avg_value
    FROM "twittertweetsentimentn"
    WHERE "Creationtime" IS NOT NULL
    GROUP BY round_time_1m("Creationtime")
    ORDER BY round_time_1m("Creationtime") ASC),

     cte_corr_crypto AS (

         SELECT round_time_1m("creationtime" AT TIME ZONE 'UTC') hour_beginning_eth, AVG("adjclose") avg_value_eth
         FROM "btctickerdata"
         WHERE "creationtime" AT TIME ZONE 'UTC' IS NOT NULL
         GROUP BY round_time_1m("creationtime" AT TIME ZONE 'UTC')
         ORDER BY round_time_1m("creationtime" AT TIME ZONE 'UTC') ASC),

     joined_data AS (

         SELECT cte_corr_sentiment.hour_beginning tm, avg_value x_at_tm, avg_value_eth y_at_tm /*corr("avg_value","avg_value_eth") AS "correlation between eth and sentiment"*/
         FROM cte_corr_sentiment INNER JOIN cte_corr_crypto ON cte_corr_sentiment.hour_beginning = cte_corr_crypto.hour_beginning_eth
         WHERE cte_corr_crypto.hour_beginning_eth >= '2022-04-06 12:59:00' ),

     delta AS (
         SELECT *
         FROM generate_series(1, 3) delta ),

     dates AS (
         SELECT
             tm AS present,
             delta,
             tm + delta * 15 * '1 minute'::INTERVAL AS future
         FROM joined_data
                  CROSS JOIN delta
     ),

     pairwise AS (
         SELECT
             dates.present,
             dates.future,
             dates.delta,
             present.x_at_tm AS present_x,
             future.y_at_tm AS future_y
         FROM
             dates,
             joined_data AS present,
             joined_data AS future
         WHERE dates.present = present.tm
           AND dates.future = future.tm
     ),

     cross_corrs AS (
         SELECT
             delta,
             CORR(present_x, future_y) AS pearson
         FROM pairwise
         GROUP BY delta
         ORDER BY delta
     )

SELECT * FROM cross_corrs;