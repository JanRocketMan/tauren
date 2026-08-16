"""Provider-neutral transcript message models.

A transcript is the conversation state that an agent and a model work with.
This module defines the message types that build a transcript:

- `UserMessage`: what the user submitted
- `AssistantMessage`: what the assistant replied, including tool calls
- `ToolResultMessage`: the result of running one tool call

`AgentMessage` is the union of all of them. Later tasks will add more
message types, and every layer above (provider, loop, CLI, sessions) will
work with `AgentMessage` objects instead of provider-specific payloads.
"""

from dataclasses import dataclass, field
from time import time

from agent.types import JSONValue


def current_timestamp_ms() -> int:
    """Return the current Unix time in milliseconds."""
    return int(time() * 1000)


@dataclass(frozen=True, slots=True)
class ToolCall:
    """A request to run a named tool with JSON arguments.

    A tool call is not the tool itself. It only records what the assistant
    asked for: a name and the arguments it wants to pass.
    """

    id: str
    name: str
    arguments: dict[str, JSONValue] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class UserMessage:
    """A message storing text submitted by the user."""

    content: str
    timestamp: int = field(default_factory=current_timestamp_ms)

    @property
    def text(self) -> str:
        """Return the visible text of this message.

        TODO(1): return the message content.
        """
        return self.content


@dataclass(frozen=True, slots=True)
class AssistantMessage:
    """A message storing assistant text and optional tool calls.

    An assistant can do two things in one turn: produce visible text and
    request tool execution. Both live on the same message.
    """

    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    timestamp: int = field(default_factory=current_timestamp_ms)

    @property
    def text(self) -> str:
        """Return the visible text of this message.

        TODO(1): return the message content.
        """
        return self.content


@dataclass(frozen=True, slots=True)
class ToolResultMessage:
    """The result of executing one tool call.

    The model needs tool results in the transcript so it can continue
    reasoning after a tool runs.
    """

    tool_call_id: str
    name: str
    content: str
    ok: bool = True
    timestamp: int = field(default_factory=current_timestamp_ms)

    @property
    def text(self) -> str:
        """Return the visible text of this message.

        TODO(1): return the message content.
        """
        return self.content


# The union of every message type. Functions can accept a transcript as
# list[AgentMessage] without caring which concrete type each item is.
type AgentMessage = UserMessage | AssistantMessage | ToolResultMessage


def message_text(message: AgentMessage) -> str:
    """Return the user-visible text represented by any agent message.

    This is the dispatch function that later layers use when they want the
    plain text of a transcript entry without switching on message types.

    TODO(1): return message.text for each concrete message type.
    """
    if isinstance(message, (UserMessage, AssistantMessage, ToolResultMessage)):
        return message.text
    else:
        raise NotImplementedError(f"Incorrect input type of message {message}")
