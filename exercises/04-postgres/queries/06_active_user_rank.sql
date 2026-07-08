WITH monthly_user_posts AS (
    SELECT
        DATE_TRUNC('month', posts.created_at) AS month,
        users.id AS user_id,
        users.username,
        COUNT(posts.id) AS post_count
    FROM users
    JOIN posts
        ON users.id = posts.user_id
    GROUP BY month, users.id, users.username
),
ranked_users AS (
    SELECT
        month,
        user_id,
        username,
        post_count,
        RANK() OVER (
            PARTITION BY month
            ORDER BY post_count DESC
        ) AS rank
    FROM monthly_user_posts
)
SELECT *
FROM ranked_users
WHERE rank = 1
ORDER BY month DESC;