from typing import Optional, Dict, Any, List, Callable, TypeVar, Type
from pydantic import BaseModel
from abc import abstractclassmethod, abstractmethod, ABC


class Command(ABC):
    """An agentscript command"""

    @classmethod
    @abstractmethod
    def type(cls) -> str:
        """Type of the command"""
        pass

    @abstractmethod
    def exec(self, data: Dict[str, Any]) -> Any:
        """Executes the command on the parsed json"""
        pass

    @classmethod
    @abstractmethod
    def json_schema(cls) -> Dict[str, Any]:
        """JSON schema for the command"""
        pass

    @classmethod
    @abstractmethod
    def model(cls) -> Type[BaseModel]:
        """Pydantic model for the command"""
        pass

    @classmethod
    @abstractmethod
    def context(cls) -> str:
        """Context for the command"""
        pass

    @classmethod
    def examples(cls) -> Optional[str]:
        """Example command usage"""
        pass

    @classmethod
    def react_component(cls) -> Optional[str]:
        """A React component to render for the command"""
        pass
