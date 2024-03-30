from typing import Optional, Dict, Any, List
import time
import uuid
import json
from enum import Enum

from toolfuse import Tool, tool
from pydantic import BaseModel

from agentscript.db.models import InvocationRecord
from agentscript.db.conn import WithDB
from agentscript.server.models import InvocationModel


class InvocationStatus(Enum):
    CREATED = "created"
    FINISHED = "finished"
    IN_PROGRESS = "in progress"
    FAILED = "failed"
    NOT_STARTED = "not started"


class Invocation(WithDB):
    """An action invocation"""

    def __init__(
        self,
        type: str,
        cmd: Dict[str, Any],
        span_index: int,
        created_time: float = time.time(),
        status: InvocationStatus = InvocationStatus.CREATED,
        finished_time: Optional[float] = None,
        result: Optional[Any] = None,
        approved: bool = False,
        message_id: Optional[str] = None,
        span_id: Optional[str] = None,
    ):
        self.type = type
        self.cmd = cmd
        self.span_index = span_index
        self.created_time = created_time
        self.status = status
        self.finished_time = finished_time
        self.id = str(uuid.uuid4())
        self.result = result
        self.approved = approved
        self.message_id = message_id
        self.span_id = span_id
        self.save()

    def to_record(self) -> InvocationRecord:
        return InvocationRecord(
            id=self.id,
            type=self.type,
            cmd=json.dumps(self.cmd),
            created_time=self.created_time,
            status=self.status.value,
            finished_time=self.finished_time,
            result=json.dumps(self.result) if self.result else None,
            approved=self.approved,
            message_id=self.message_id,
            span_index=self.span_index,
        )

    @classmethod
    def from_record(cls, record: InvocationRecord) -> "Invocation":
        obj = cls.__new__(cls)
        obj.id = record.id
        obj.span_id = record.span_id
        obj.type = record.type
        obj.cmd = json.loads(record.cmd)
        obj.created_time = record.created_time
        obj.status = InvocationStatus(record.status)
        obj.finished_time = record.finished_time
        obj.result = json.loads(record.result) if record.result else None
        obj.approved = record.approved
        obj.message_id = record.message_id
        obj.span_index = record.span_index
        return obj

    def save(self) -> None:
        for db in self.get_db():
            record = self.to_record()
            db.merge(record)
            db.commit()

    @classmethod
    def find(cls, **kwargs) -> List["Invocation"]:
        invocations = []
        for db in cls.get_db():
            records = db.query(InvocationRecord).filter_by(**kwargs).all()
            for record in records:
                invocation = cls.from_record(record)
                invocations.append(invocation)
        return invocations

    def to_schema(self) -> InvocationModel:
        """Converts an Invocation instance to its Pydantic schema representation."""
        return InvocationModel(
            id=self.id,
            type=self.type,
            cmd=self.cmd,
            span_index=self.span_index,
            created_time=self.created_time,
            status=self.status.value,
            finished_time=self.finished_time,
            result=self.result,
            approved=self.approved,
            message_id=self.message_id,
        )
