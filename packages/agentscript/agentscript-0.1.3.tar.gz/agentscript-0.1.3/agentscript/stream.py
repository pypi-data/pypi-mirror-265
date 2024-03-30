from typing import Optional, List
import time
import uuid

from .db.models import StreamRecord
from .db.conn import WithDB
from .invoke import Invocation


class Stream(WithDB):
    """A stream"""

    def __init__(self, id: Optional[str] = None):
        if not id:
            id = str(uuid.uuid4())
        self.id = id
        self.created_time: float = time.time()
        self.updated_time: float = time.time()
        self.closed_time: Optional[float] = None
        self.accumulated: str = ""
        self.invocations: List[Invocation] = []

        self.save()

    @classmethod
    def find_or_create(cls, id: str) -> "Stream":
        for db in cls.get_db():
            record = db.query(StreamRecord).filter(StreamRecord.id == id).first()
            if record:
                return cls.from_record(record)
        return cls(id=id)

    def to_record(self) -> StreamRecord:
        return StreamRecord(
            id=self.id,
            created_time=self.created_time,
            updated_time=self.updated_time,
            closed_time=self.closed_time,
            accumulated=self.accumulated,
        )

    def save(self) -> None:
        for db in self.get_db():
            record = self.to_record()
            db.merge(record)
            db.commit()

    @classmethod
    def from_record(cls, record: StreamRecord) -> "Stream":
        obj = cls.__new__(cls)  # Avoid calling __init__ during loading from record
        obj.id = record.id
        obj.created_time = record.created_time
        obj.updated_time = record.updated_time
        obj.closed_time = record.closed_time
        obj.accumulated = record.accumulated
        obj.invocations = [
            Invocation.from_record(inv_record) for inv_record in record.invocations
        ]  # Load invocations
        return obj

    def close(self) -> None:
        self.closed_time = time.time()
        self.save()

    def accumulate(self, text: str) -> None:
        """Accumulate stream text"""
        self.accumulated += text
        self.updated_time = time.time()
        self.save()

    def save(self) -> None:
        for db in self.get_db():
            record = self.to_record()
            db.merge(record)
            db.commit()
            for invocation in self.invocations:  # Save each invocation
                invocation.save()

    def add_invocation(self, invocation: Invocation) -> None:
        self.invocations.append(invocation)
        self.save()

    def remove_invocation(self, invocation_id: str) -> None:
        self.invocations = [inv for inv in self.invocations if inv.id != invocation_id]
        self.save()
