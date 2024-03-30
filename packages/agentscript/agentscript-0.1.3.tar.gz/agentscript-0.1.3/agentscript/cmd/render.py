from typing import Optional, Dict, Any
from pydantic import BaseModel


class RenderInlineModel(BaseModel):
    tool: str
    action: str
    parameters: Optional[Dict[str, Any]] = None


class RenderWindowModel(BaseModel):
    tool: str
    action: str
    parameters: Optional[Dict[str, Any]] = None
