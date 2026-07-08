SELECT
    id,
    title,
    created_at
FROM posts
WHERE status = 'published'
ORDER BY created_at DESC;