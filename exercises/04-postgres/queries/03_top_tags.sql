SELECT
    tags.name,
    COUNT(post_tags.post_id) AS post_count
FROM tags
JOIN post_tags
    ON tags.id = post_tags.tag_id
GROUP BY tags.id, tags.name
ORDER BY post_count DESC
LIMIT 5;