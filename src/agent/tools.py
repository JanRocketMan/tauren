"""Provider-neutral tool definitions and execution results.

Tools are how the assistant asks the agent to touch the environment. A tool
has two parts:

- `AgentTool`: the description of a tool the model may call. It carries a
  name, a description, an input schema, and an async executor
- `AgentToolResult`: the structured output of running one tool call

`ToolCall` already lives in `agent/messages.py`: it is what the assistant
records when it asks for a tool. `AgentTool` is what the agent knows how to
run. The future agent loop will match each `ToolCall` to an `AgentTool` by
name, run its executor, and convert the result into a `ToolResultMessage`
on the transcript.

This module stays portable. It must not mention providers, the CLI, or any
frontend.
"""

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass

from agent.types import JSONObject, JSONValue


@dataclass(frozen=True, slots=True)
class AgentToolResult:
    """The structured output of running one tool call.

    The fields mirror `ToolResultMessage` from `agent/messages.py` without
    the timestamp. The loop stamps the timestamp when it converts a result
    into a transcript message, because time is a transcript concern, not a
    tool concern.
    """

    tool_call_id: str
    name: str
    content: str
    ok: bool = True

    @property
    def text(self) -> str:
        """Return the visible text of this result.

        TODO(2): return the result content.
        """
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class AgentTool:
    """A tool exposed to the portable agent loop.

    `name` and `description` tell the model what it may call. `input_schema`
    describes the JSON arguments the tool accepts. `executor` runs the tool
    when the loop asks for it.
    """

    name: str
    description: str
    input_schema: JSONObject
    executor: Callable[[str, Mapping[str, JSONValue]], Awaitable[AgentToolResult]]

    async def execute(
        self,
        tool_call_id: str,
        arguments: Mapping[str, JSONValue],
    ) -> AgentToolResult:
        """Run this tool for one tool call.

        The loop supplies the call id so the result can be matched back to
        the assistant's request.

        TODO(2): delegate to the executor and await it.
        """
        raise NotImplementedError
