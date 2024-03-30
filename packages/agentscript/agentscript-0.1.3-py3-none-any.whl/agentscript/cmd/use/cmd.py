from typing import Optional, Dict, Any, List, Callable, TypeVar, Type
from pydantic import BaseModel
import inspect

from toolfuse import Tool, tool_from_object, tool_from_function

from ..base import Command


class UseCommand(BaseModel):
    tool: str
    action: str
    parameters: Optional[Dict[str, Any]] = None


class Use(Command):
    """Use a tool"""

    def __init__(self, tools: List[Tool | Callable | Any], approve: bool = False):
        self.tools = {}
        for tool_ in tools:
            if not isinstance(tool_, Tool):
                print("converting to tool")
                if inspect.isclass(input):
                    raise ValueError(
                        "Cannot pass a class to the 'use' command, must be a function, tool, or object"
                    )
                if inspect.isfunction(tool_):
                    tool_ = tool_from_function(tool_)()
                else:
                    tool_ = tool_from_object(tool_)
            self.tools[tool_.name()] = tool_
        self.approve = approve

    @classmethod
    def type(cls) -> str:
        return "use"

    @classmethod
    def json_schema(cls) -> Dict[str, Any]:
        """JSON schema for the command"""
        return UseCommand.model_json_schema()

    @classmethod
    def model(cls) -> Type[BaseModel]:
        """Pydantic model for the command"""
        return UseCommand

    @classmethod
    def context(cls) -> str:
        """Context for the command"""
        return (
            "The 'use' command type allows you to use tools. You will be "
            "given a list of tools which you can use. Your job is to select "
            "the tool and action you want to use."
        )

    @classmethod
    def examples(cls) -> Optional[str]:
        """Example command usage"""
        return [
            'I need to check the weather <{"type": "use", "tool": "Weather", "action": "current", "parameters": {"city": "London"}}>',
            'I need to ask the user if they want to continue <{"type": "use", "tool": "Chat", "action": "boolean", "parameters": {"message": "Do you want to continue?"}}>',
        ]

    def exec(self, data: Dict[str, Any]) -> Any:
        cmd = self.parse(data)
        return self._exec(cmd)

    def parse(self, data: dict) -> UseCommand:
        cmd = UseCommand(tool=data["tool"], action=data["action"])
        if "parameters" in data:
            cmd.parameters = data["parameters"]
        return cmd

    def _exec(self, command: UseCommand) -> Any:
        tool: Tool = self.tools.get(command.tool)
        if not tool:
            raise Exception(f"Tool {command.tool} not found")
        action = tool.find_action(command.action)
        if not action:
            raise (Exception(f"Action {command.action} not found"))
        result = tool.use(action, **command.parameters)
        return result

    @classmethod
    def react_component(cls) -> Optional[str]:
        """A React component to render for the command"""
        pass
