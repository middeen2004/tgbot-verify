"""In-memory pending verification sessions with TTL."""
import time
from typing import Dict, Optional

TTL_SECONDS = 300  # 5 minutes
_pending: Dict[int, Dict[str, float]] = {}


def set_pending(user_id: int, command_key: str) -> None:
    _pending[user_id] = {"command": command_key, "created_at": time.time()}


def get_pending(user_id: int) -> Optional[Dict[str, float]]:
    entry = _pending.get(user_id)
    if not entry:
        return None
    if time.time() - entry.get("created_at", 0) > TTL_SECONDS:
        _pending.pop(user_id, None)
        return None
    return entry


def clear_pending(user_id: int) -> None:
    _pending.pop(user_id, None)


def ttl_remaining(user_id: int) -> int:
    entry = _pending.get(user_id)
    if not entry:
        return 0
    return max(0, int(TTL_SECONDS - (time.time() - entry.get("created_at", 0))))
