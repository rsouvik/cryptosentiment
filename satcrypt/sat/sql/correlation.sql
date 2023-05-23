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
         ORDER BY round_time_1m("creationtime" AT TIME ZONE 'UTC') ASC)

SELECT corr("avg_value","avg_value_eth") AS "correlation between eth and sentiment"
FROM cte_corr_sentiment INNER JOIN cte_corr_crypto ON cte_corr_sentiment.hour_beginning = cte_corr_crypto.hour_beginning_eth;