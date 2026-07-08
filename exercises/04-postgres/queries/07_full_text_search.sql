SELECT
    id,
    title,
    body
FROM posts
WHERE to_tsvector('english', body) @@ plainto_tsquery('english', 'database');