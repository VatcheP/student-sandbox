import os

from fastapi import Header, HTTPException, status


def verify_api_key(
    x_api_key: str | None = Header(default=None),
) -> str:
    expected_api_key = os.getenv("API_KEY")

    if expected_api_key is None:
        raise RuntimeError("API_KEY environment variable is not set")

    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

    return x_api_key