# Exercise 04 - PostgreSQL Schema

## Overview

This project demonstrates:

- PostgreSQL running in Docker
- Schema design with primary keys and foreign keys
- Constraints and indexes
- SQL joins and aggregations
- Window functions
- Query optimization using EXPLAIN ANALYZE

## Schema

Tables:

- users
- posts
- comments
- tags
- post_tags

Relationships:

- User -> Posts (1:M)
- User -> Comments (1:M)
- Post -> Comments (1:M)
- Post -> Tags (M:M through post_tags)

## Running

Start database:

```bash
docker compose up -d

Apply migrations:
Get-Content .\migrations\001_initial.sql | docker exec -i exercise04-postgres psql -U postgres -d exercise04
Apply indexes:
Get-Content .\migrations\002_add_indexes.sql | docker exec -i exercise04-postgres psql -U postgres -d exercise04
Seed database:
Get-Content .\seed.sql | docker exec -i exercise04-postgres psql -U postgres -d exercise04


Queries
Recent posts
Posts with comment count
Top tags by usage
Users posting within last 7 days
Comment threads
Most active user per month
Full text search
Posts with no comments

Index
CREATE INDEX idx_comments_post_id
ON comments(post_id);
Purpose:

Speed up joins between posts and comments.

For small datasets PostgreSQL still chose a sequential scan because scanning 200 rows is cheaper than traversing a B-tree index.