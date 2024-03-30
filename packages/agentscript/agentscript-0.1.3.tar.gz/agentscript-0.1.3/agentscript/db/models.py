from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Float,
    Integer,
    Boolean,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class StreamRecord(Base):
    __tablename__ = "streams"

    id = Column(String, primary_key=True)
    created_time = Column(Float)
    updated_time = Column(Float)
    closed_time = Column(Float, nullable=True)
    accumulated = Column(String)
    # Establish a relationship to InvocationRecord with back_populates
    invocations = relationship("InvocationRecord", back_populates="stream")


class InvocationRecord(Base):
    __tablename__ = "invocations"

    id = Column(String, primary_key=True)
    type = Column(String)
    cmd = Column(String)
    created_time = Column(Float)
    status = Column(String)
    finished_time = Column(Float, nullable=True)
    result = Column(String, nullable=True)
    approved = Column(Boolean)
    message_id = Column(String, nullable=True)
    span_index = Column(Integer)
    stream_id = Column(String, ForeignKey("streams.id"))
    # Define the relationship back to StreamRecord
    stream = relationship("StreamRecord", back_populates="invocations")
