SELECT
    posts.id AS post_id,
    posts.title,
    comments.id AS comment_id,
    users.username AS commenter,
    comments.body,
    comments.created_at
FROM posts
JOIN comments
    ON posts.id = comments.post_id
JOIN users
    ON comments.user_id = users.id
ORDER BY posts.id, comments.created_at;