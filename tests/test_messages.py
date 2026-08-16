"""Tests for the core transcript message models.

These tests are the contract for task 01. Make them pass by feeding the
TODO(1) pieces in `src/agent/messages.py`.
"""

from agent.messages import (
    AgentMessage,
    AssistantMessage,
    ToolCall,
    ToolResultMessage,
    UserMessage,
    message_text,
)


def test_user_message_holds_prompt() -> None:
    msg = UserMessage(content="Read README.md")
    assert msg.content == "Read README.md"
    assert msg.text == "Read README.md"


def test_assistant_message_holds_text_and_tool_calls() -> None:
    call = ToolCall(id="call-1", name="read", arguments={"path": "README.md"})
    msg = AssistantMessage(content="I will inspect the file.", tool_calls=[call])
    assert msg.text == "I will inspect the file."
    assert msg.tool_calls == [call]
    assert msg.tool_calls[0].name == "read"


def test_tool_call_defaults_to_empty_arguments() -> None:
    call = ToolCall(id="call-1", name="write")
    assert call.arguments == {}


def test_tool_call_arguments_accept_nested_json() -> None:
    call = ToolCall(
        id="call-1",
        name="edit",
        arguments={"path": "a.py", "edits": [1, 2, {"x": None}]},
    )
    edits = call.arguments["edits"]
    assert isinstance(edits, list)
    assert edits[2] == {"x": None}


def test_tool_result_defaults_to_success() -> None:
    ok_result = ToolResultMessage(tool_call_id="call-1", name="read", content="file body")
    assert ok_result.ok is True
    assert ok_result.text == "file body"

    failed = ToolResultMessage(tool_call_id="call-2", name="bash", content="boom", ok=False)
    assert failed.ok is False


def test_message_text_dispatches_on_type() -> None:
    transcript: list[AgentMessage] = [
        UserMessage(content="hi"),
        AssistantMessage(content="hello", tool_calls=[ToolCall(id="c1", name="read")]),
        ToolResultMessage(tool_call_id="c1", name="read", content="file body"),
    ]
    assert [message_text(m) for m in transcript] == ["hi", "hello", "file body"]
