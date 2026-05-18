"""
Security utilities — rate limiting, input sanitization.
"""

import time
from collections import defaultdict
from fastapi import HTTPException, Request

from app.core.config import settings


class RateLimiter:
    """Simple in-memory rate limiter per IP address."""

    def __init__(self, max_requests: int = settings.RATE_LIMIT_PER_MINUTE, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def check(self, request: Request) -> None:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Bersihkan timestamp yang sudah kedaluwarsa
        self._requests[client_ip] = [
            t for t in self._requests[client_ip] if now - t < self.window
        ]

        if len(self._requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Terlalu banyak permintaan. Coba lagi nanti.",
            )

        self._requests[client_ip].append(now)


rate_limiter = RateLimiter()


def sanitize_text(text: str, max_length: int = 5000) -> str:
    """Sanitize user input text — trim dan batasi panjang."""
    if not text:
        return ""
    return text.strip()[:max_length]
