from typing import Optional, Any, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..models.activity_logs import ActivityLog
from ..schemas.activity_logs import ActivityLogCreateSchema
from ..core.loggers import db_logger as logger


class CRUDActivityLog(
    CRUDBase[ActivityLog, ActivityLogCreateSchema, ActivityLogCreateSchema]
):
    """
    CRUD operations for Activity Logs in AutoMeet.
    Used to track user actions such as create, update, and delete events.
    """

    async def _remove_sensitive_data(
        self, data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Remove sensitive fields from activity log snapshots.
        """
        if not data:
            return data

        sensitive_keys = ["password", "hashed_password"]

        cleaned_data = data.copy()
        for key in sensitive_keys:
            if key in cleaned_data:
                cleaned_data[key] = "********"

        return cleaned_data

    async def changes_made(
        self,
        previous_data: Optional[Dict[str, Any]],
        new_data: Optional[Dict[str, Any]],
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        Compare previous and new data to extract exact changes.
        """
        if previous_data is None and new_data is None:
            return None, None

        previous_data = await self._remove_sensitive_data(previous_data)
        new_data = await self._remove_sensitive_data(new_data)

        if previous_data is None:
            return None, new_data

        if new_data is None:
            return previous_data, None

        previous_changes: Dict[str, Any] = {}
        new_changes: Dict[str, Any] = {}

        all_keys = set(previous_data.keys()) | set(new_data.keys())

        for key in all_keys:
            old_value = previous_data.get(key)
            new_value = new_data.get(key)

            if old_value != new_value:
                if old_value is not None:
                    previous_changes[key] = old_value
                if new_value is not None:
                    new_changes[key] = new_value

        return previous_changes or None, new_changes or None

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: ActivityLogCreateSchema
    ) -> ActivityLog:
        """
        Create a new activity log entry in AutoMeet.
        """
        db_obj = self.model(**obj_in.model_dump())

        # Normalize snapshot changes
        previous_changes, new_changes = await self.changes_made(
            previous_data=db_obj.previous_data,
            new_data=db_obj.new_data,
        )

        db_obj.previous_data = previous_changes or {}
        db_obj.new_data = new_changes or {}

        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj

        except Exception as exc:
            await db.rollback()
            logger.error(f"Failed to create activity log: {exc}")
            raise RuntimeError("Could not create activity log") from exc


activity_log_crud = CRUDActivityLog(ActivityLog)
