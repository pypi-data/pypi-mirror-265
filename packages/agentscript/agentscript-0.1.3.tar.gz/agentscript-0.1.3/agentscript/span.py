from typing import List, Optional
import time
import uuid

from agentscript.db.models import SpanRecord
from agentscript.db.conn import WithDB
from agentscript.server.models import SpanModel
from .invoke import Invocation


class Span(WithDB):
    """A class to represent a span of text, which can have multiple invocations."""

    def __init__(
        self, text: str, created_time: Optional[float] = None, id: Optional[str] = None
    ):
        self.text = text
        if not id:
            id = str(uuid.uuid4())
        self.id = id
        self.created_time: float = created_time if created_time else time.time()
        self.invocations: List[Invocation] = []

    @classmethod
    def from_record(cls, record: SpanRecord) -> "Span":
        obj = cls.__new__(cls)  # Create an instance without calling __init__
        obj.id = record.id
        obj.created_time = record.created_time
        obj.text = record.text
        obj.invocations = [
            Invocation.from_record(inv_record) for inv_record in record.invocations
        ]
        return obj

    def to_record(self) -> SpanRecord:
        return SpanRecord(
            id=self.id,
            created_time=self.created_time,
            text=self.text,
        )

    def save(self) -> None:
        for db in self.get_db():
            record = self.to_record()
            db.merge(record)
            db.commit()
            for invocation in self.invocations:
                invocation.span_id = self.id
                invocation.save()

    def add_invocation(self, invocation: Invocation) -> None:
        self.invocations.append(invocation)
        self.save()

    @classmethod
    def find(cls, **kwargs) -> List["Span"]:
        Messages = []
        for db in cls.get_db():
            records = db.query(SpanRecord).filter_by(**kwargs).all()
            for record in records:
                Message = cls.from_record(record)
                Messages.append(Message)
        return Messages

    def to_schema(self) -> SpanModel:
        """Converts an Message instance to its Pydantic schema representation."""
        return SpanModel(
            id=self.id,
            created_time=self.created_time,
            text=self.text,
            invocations=[invocation.to_schema() for invocation in self.invocations],
        )
