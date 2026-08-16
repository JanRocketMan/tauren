"""Tests for the agent event models.

These tests are the contract for task 02's `events.py`. Build the event
classes and the `AgentEvent` union from the spec table in the task doc.
"""

from agent.events import (
    AgentEndEvent,
    AgentEvent,
    AgentStartEvent,
    MessageDeltaEvent,
    MessageEndEvent,
    MessageStartEvent,
    ToolExecutionEndEvent,
    ToolExecutionStartEvent,
    ToolExecutionUpdateEvent,
    TurnEndEvent,
    TurnStartEvent,
)

from agent.messages import AssistantMessage, ToolResultMessage, UserMessage
from agent.tools import AgentToolResult


def test_start_and_end_events_have_stable_types() -> None:
    assert AgentStartEvent().type == "agent_start"
    assert AgentEndEvent().type == "agent_end"


def test_agent_end_carries_the_transcript() -> None:
    end = AgentEndEvent(messages=[UserMessage(content="hi")])
    assert end.type == "agent_end"
    assert end.messages[0].text == "hi"


def test_turn_end_carries_message_and_tool_results() -> None:
    message = AssistantMessage(content="done")
    result = ToolResultMessage(tool_call_id="call-1", name="read", content="file body")
    end = TurnEndEvent(message=message, tool_results=[result])
    assert end.type == "turn_end"
    assert end.message.text == "done"
    assert end.tool_results[0].name == "read"


def test_message_events_carry_start_snapshot_and_text_deltas() -> None:
    prompt = UserMessage(content="please read README.md")
    start = MessageStartEvent(message=prompt)
    delta = MessageDeltaEvent(text="I will read it.")
    end = MessageEndEvent(message=AssistantMessage(content="I will read it."))
    assert [start.type, delta.type, end.type] == [
        "message_start",
        "message_delta",
        "message_end",
    ]
    assert start.message.content == "please read README.md"
    assert delta.text == "I will read it."
    assert end.message.content == "I will read it."


def test_tool_execution_events_carry_progress() -> None:
    start = ToolExecutionStartEvent(
        tool_call_id="call-1", tool_name="read", args={"path": "README.md"}
    )
    result = AgentToolResult(tool_call_id="call-1", name="read", content="file body")
    update = ToolExecutionUpdateEvent(
        tool_call_id="call-1", tool_name="read", partial_result=result
    )
    end = ToolExecutionEndEvent(
        tool_call_id="call-1", tool_name="read", result=result, is_error=False
    )
    assert start.type == "tool_execution_start"
    assert start.args["path"] == "README.md"
    assert update.partial_result.text == "file body"
    assert end.is_error is False


def test_agent_event_union_accepts_every_concrete_type() -> None:
    transcript = [UserMessage(content="hi")]
    delta = MessageDeltaEvent(text="hi")
    result = AgentToolResult(tool_call_id="c1", name="read", content="file body")
    events: list[AgentEvent] = [
        AgentStartEvent(),
        TurnStartEvent(),
        MessageStartEvent(message=transcript[0]),
        delta,
        MessageEndEvent(message=transcript[0]),
        TurnEndEvent(message=transcript[0]),
        ToolExecutionStartEvent(tool_call_id="c1", tool_name="read"),
        ToolExecutionUpdateEvent(tool_call_id="c1", tool_name="read", partial_result=result),
        ToolExecutionEndEvent(tool_call_id="c1", tool_name="read", result=result, is_error=False),
        AgentEndEvent(messages=transcript),
    ]
    assert [e.type for e in events] == [
        "agent_start",
        "turn_start",
        "message_start",
        "message_delta",
        "message_end",
        "turn_end",
        "tool_execution_start",
        "tool_execution_update",
        "tool_execution_end",
        "agent_end",
    ]
