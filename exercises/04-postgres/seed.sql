INSERT INTO users (username, email)
SELECT
    'user' || n,
    'user' || n || '@example.com'
FROM generate_series(1, 10) AS n;

INSERT INTO posts (user_id, title, body, status, created_at)
SELECT
    ((n - 1) % 10) + 1,
    'Post ' || n,
    'This is the body of post ' || n || '. It talks about databases, Docker, SQL, and backend systems.',
    CASE WHEN n % 5 = 0 THEN 'draft' ELSE 'published' END,
    NOW() - (n || ' days')::interval
FROM generate_series(1, 50) AS n;

INSERT INTO comments (post_id, user_id, body, created_at)
SELECT
    ((n - 1) % 50) + 1,
    ((n - 1) % 10) + 1,
    'Comment ' || n || ' on a post.',
    NOW() - (n || ' hours')::interval
FROM generate_series(1, 200) AS n;

INSERT INTO tags (name)
SELECT 'tag' || n
FROM generate_series(1, 20) AS n;

INSERT INTO post_tags (post_id, tag_id)
SELECT DISTINCT
    ((n - 1) % 50) + 1,
    ((n - 1) % 20) + 1
FROM generate_series(1, 100) AS n;