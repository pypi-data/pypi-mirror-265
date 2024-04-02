SOCIAL_INTELLIGENCE_READ_DB_SECRET_ID = "social-intelligence-read-db"

GET_TOKEN_DETAILS_FROM_SYMBOL_QUERY = """
WITH tokens AS (
    SELECT "eth" AS chain, p.token_id, p.latest_liquidity_usd, p.latest_market_cap, 
    (pop.buy_vol_24_hr_usd + pop.sell_vol_24_hr_usd) AS vol_24_hr, token_symbol
    FROM social.pairs AS p
    LEFT JOIN social.pairs_onchain_properties AS pop
    ON p.pair_id = pop.pair_id
    WHERE p.token_symbol = %(symbol)s
    HAVING vol_24_hr > 0
    UNION ALL
    SELECT chain, address AS token_id, liquidity, marketcap, vol24hUSD AS vol_24_hr,
    symbol AS token_symbol
    FROM blockchains.tokens 
    WHERE symbol = %(symbol)s
    HAVING vol_24_hr > 0
)
SELECT * 
FROM tokens
ORDER BY vol_24_hr DESC
LIMIT %(limit)s
"""

GET_TOKEN_SYMBOL_FOR_MULTIPLE_SYMBOLS_QUERY = """
WITH tokens AS (
    SELECT "eth" AS chain, p.token_id, p.latest_liquidity_usd, p.latest_market_cap, 
    (pop.buy_vol_24_hr_usd + pop.sell_vol_24_hr_usd) AS vol_24_hr, p.token_symbol
    FROM social.pairs AS p
    LEFT JOIN social.pairs_onchain_properties AS pop
    ON p.pair_id = pop.pair_id
    WHERE p.token_symbol IN {symbols}
    HAVING vol_24_hr > 0
    UNION ALL
    SELECT chain, address AS token_id, liquidity, marketcap, vol24hUSD AS vol_24_hr, symbol AS token_symbol
    FROM blockchains.tokens 
    WHERE symbol IN {symbols}
    HAVING vol_24_hr > 0
)
SELECT * 
FROM (
    SELECT *,
    DENSE_RANK() OVER (PARTITION BY token_symbol ORDER BY vol_24_hr DESC) AS token_rank
    FROM tokens
    ORDER BY vol_24_hr DESC
) AS sub
WHERE token_rank <= %(limit)s
"""