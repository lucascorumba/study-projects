-- SQL statement to build the inverted index - also in the .sql file
CREATE INDEX gin ON tweet USING gin (to_tsvector('portuguese', body));
-- DROP INDEX gin;

-- query examples
SELECT count(id), max(created_at), min(created_at) FROM tweets;

SELECT count(id) FROM tweet WHERE to_tsquery('portuguese', 'eleição') @@ to_tsvector('portuguese', body);
SELECT count(id) FROM tweet WHERE to_tsquery('portuguese', 'voto') @@ to_tsvector('portuguese', body);
-- SELECT count(id) FROM tweet WHERE to_tsquery('portuguese', 'batata') @@ to_tsvector('portuguese', body);


-- comparing index vs. no index
EXPLAIN ANALYZE SELECT count(id) FROM tweet WHERE body LIKE '%voto%';
EXPLAIN ANALYZE SELECT count(id) FROM tweet WHERE to_tsquery('portuguese', 'voto') @@ to_tsvector('portuguese', body);

-- ranking
SELECT id, ts_rank(to_tsvector('portuguese', body), to_tsquery('portuguese', 'voto')) as ts_rank
FROM tweet
WHERE to_tsquery('portuguese', 'voto') @@ to_tsvector('portuguese', body)
ORDER BY ts_rank DESC
LIMIT 10;

