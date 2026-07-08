SELECT
    posts.id,
    posts.title
FROM posts
LEFT JOIN comments
    ON posts.id = comments.post_id
WHERE comments.id IS NULL
ORDER BY posts.id;