from typing import List, Optional
import time
import json
import re
import uuid

from .invoke import Invocation, InvocationStatus
from .cmd import Command
from .stream import Stream


class Parser:
    """An agentscript parser"""

    def parse(self, command: str) -> List[dict]:
        json_str_matches = re.findall(r"<(\{.*?\})>", command)
        print("json_str_matches: ", json_str_matches)
        parsed_json_objects = []
        for json_str in json_str_matches:
            try:
                jdict = json.loads(json_str)
                parsed_json_objects.append(jdict)
            except Exception as e:
                print(f"Error decoding JSON: {e}")

        return parsed_json_objects


class Interpreter:
    """An agentscript interpreter"""

    # TODO: should this also just take functions
    def __init__(self, commands: List[Command], approve: bool = False):
        self.commands = {cmd.type(): cmd for cmd in commands}
        self.approve = approve
        self._invocations: List[Invocation] = []
        self._id = str(uuid.uuid4())
        self._parser = Parser()

    def execute(self, text: str, stream_id: Optional[str] = None) -> Stream:
        stream = Stream.find_or_create(stream_id)
        print("id: ", id)
        print("msg: ", text)
        print("executing msg: ", text)
        print("stream: ", stream)
        stream.accumulate(text)
        dicts = self._parser.parse(text)
        print("dicts: ", dicts)

        # You are here, you need to work the stream into the rest of this method
        for i, data in enumerate(dicts):
            print("data: ", data)
            if "type" not in data:
                raise ValueError(f"parsed command without a type: {data}")
            cmd_type = data["type"]
            print("cmd_type: ", cmd_type)
            cmd = self.commands.get(cmd_type)
            if not cmd:
                raise ValueError(f"Unknown command type {data['type']}")
            print("cmd: ", cmd.__dict__)
            invocation = Invocation(type=cmd_type, cmd=data, span_index=i)

            # check to see if the invocation has already happened based on the index
            if len(stream.invocations) >= i + 1:
                print("invocation already happened")
                continue

            stream.add_invocation(invocation)
            self._invocations.append(invocation)
            invocation.status = InvocationStatus.IN_PROGRESS
            try:
                print("executing command")
                result = cmd.exec(data)
                print("result: ", result)
            except Exception as e:
                print(f"Error executing command: {e}")
                result = None
                invocation.status = InvocationStatus.FAILED
                invocation.result = e
                raise e

            invocation.finished_time = time.time()
            invocation.result = result
            invocation.status = InvocationStatus.FINISHED

        return stream

    def invocations(self) -> List[Invocation]:
        return self._invocations

    def system_prompt(self) -> str:
        pass
