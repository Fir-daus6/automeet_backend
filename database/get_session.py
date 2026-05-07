"""Re-export async session dependency (some modules expect this path)."""

from app.database.database import get_async_session

__all__ = ["get_async_session"]
