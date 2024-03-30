from typing import Optional, List, Dict, Any

from pydantic import BaseModel


class InvocationModel(BaseModel):
    id: str
    function: str
    parameters: Dict[str, Any]
    index: int
    created_time: float
    status: str
    finished_time: Optional[float] = None
    result: Optional[Any] = None
    approved: bool = False
    span_id: Optional[str] = None
    message_id: Optional[str] = None


class InvocationsModel:
    invocations: List[InvocationModel] = []


class SpanModel(BaseModel):
    id: str
    created_time: float
    text: str
    invocations: List[InvocationModel] = []


class MessagesModel:
    spans: List[SpanModel] = []
