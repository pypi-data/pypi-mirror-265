from typing import Optional, Dict, Any, List, Callable, TypeVar, Type
import time
import uuid
import json
import re
from enum import Enum
from pydantic import BaseModel
from abc import abstractclassmethod, abstractmethod, ABC


class CommandParser(BaseModel):
    """An agentscript command"""

    def __init__(self, types: List[Command] = []):
        self.types = types

    def parse(self, str: str) -> Optional["CommandType"]:
        try:
            jdict = json.loads(str)
            self.type = jdict["type"]
        except:
            return None
        for type in self.types:
            if type.__name__ == self.type:
                return type.parse(jdict)
        raise ValueError(f"Unknown command type {self.type}")
