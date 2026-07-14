from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.db import get_db
from app.models import Post
from app.schemas import PostIn, PostOut, PostUpdate


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("", response_model=list[PostOut])
def get_posts(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    post_status: Literal["draft", "published"] | None = Query(
        default=None,
        alias="status",
    ),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * per_page

    statement = select(Post).order_by(Post.id)

    if post_status is not None:
        statement = statement.where(Post.status == post_status)

    statement = statement.offset(offset).limit(per_page)

    return db.scalars(statement).all()


@router.get("/{post_id}", response_model=PostOut)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return post


@router.post(
    "",
    response_model=PostOut,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    post_data: PostIn,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    post = Post(
        user_id=post_data.user_id,
        title=post_data.title,
        body=post_data.body,
        status=post_data.status,
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.patch("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    post = db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    updates = post_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)

    return post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    post = db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)