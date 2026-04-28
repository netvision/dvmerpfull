import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy.orm import Session

from models import AuditLog


def _json_default(value: Any):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    return str(value)


def _to_json(payload: Optional[dict[str, Any]]) -> Optional[str]:
    if payload is None:
        return None
    return json.dumps(payload, default=_json_default, ensure_ascii=True, separators=(",", ":"))


def write_audit_log(
    db: Session,
    *,
    actor_user_id: Optional[int],
    entity_type: str,
    entity_id: str,
    action: str,
    change_summary: Optional[str] = None,
    before_payload: Optional[dict[str, Any]] = None,
    after_payload: Optional[dict[str, Any]] = None,
    ip_address: Optional[str] = None,
) -> None:
    row = AuditLog(
        actor_user_id=actor_user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        change_summary=change_summary,
        before_payload=_to_json(before_payload),
        after_payload=_to_json(after_payload),
        ip_address=ip_address,
    )
    db.add(row)
