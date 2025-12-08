from datetime import datetime, timezone

from src.Domain_Layer.Entities.AuditLog import AuditLog


def test_auditlog_entity_attributes():
    now = datetime.now(timezone.utc)
    a = AuditLog(log_id=None, user_id=5, timestamp=now)
    assert a.log_id is None
    assert a.user_id == 5
    assert a.timestamp is now
