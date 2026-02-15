"""HTTP client for the Mango Reach API.

Provides a shared async client that forwards the user's JWT token
to authenticate requests against the Mango Reach backend.
"""

import httpx
import os
import logging

logger = logging.getLogger(__name__)

MANGO_REACH_API_URL = os.getenv("MANGO_REACH_API_URL", "http://localhost:8008")
_BASE = f"{MANGO_REACH_API_URL}/api/v1"


def _get_headers(token: str) -> dict:
    """Build auth headers from the user's JWT."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


async def api_get(path: str, token: str, params: dict | None = None) -> dict:
    """GET request to Mango Reach API."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{_BASE}{path}"
        logger.info(f"GET {url}")
        resp = await client.get(url, headers=_get_headers(token), params=params)
        resp.raise_for_status()
        return resp.json()


async def api_post(path: str, token: str, body: dict) -> dict:
    """POST request to Mango Reach API."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{_BASE}{path}"
        logger.info(f"POST {url}")
        resp = await client.post(url, headers=_get_headers(token), json=body)
        resp.raise_for_status()
        return resp.json()


async def api_patch(path: str, token: str, body: dict) -> dict:
    """PATCH request to Mango Reach API."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{_BASE}{path}"
        logger.info(f"PATCH {url}")
        resp = await client.patch(url, headers=_get_headers(token), json=body)
        resp.raise_for_status()
        return resp.json()
