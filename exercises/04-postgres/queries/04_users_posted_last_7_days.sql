SELECT DISTINCT
    users.id,
    users.username
FROM users
JOIN posts
    ON users.id = posts.user_id
WHERE posts.created_at >= NOW() - INTERVAL '7 days'
ORDER BY users.username;