SELECT
    posts.id,
    posts.title,
    COUNT(comments.id) AS comment_count
FROM posts
LEFT JOIN comments
    ON posts.id = comments.post_id
GROUP BY posts.id, posts.title
ORDER BY comment_count DESC;