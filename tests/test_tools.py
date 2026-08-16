"""Tests for the portable tool model.

These tests are the contract for task 02's `tools.py`. Make them pass by
feeding the TODO(2) pieces in `src/agent/tools.py`.
"""

import asyncio
from collections.abc import Mapping

from agent.tools import AgentTool, AgentToolResult
from agent.types import JSONValue


def test_agent_tool_result_defaults_to_success() -> None:
    result = AgentToolResult(tool_call_id="call-1", name="read", content="file body")
    assert result.ok is True
    assert result.text == "file body"


def test_agent_tool_result_can_report_failure() -> None:
    failed = AgentToolResult(tool_call_id="call-2", name="bash", content="boom", ok=False)
    assert failed.ok is False


def test_agent_tool_runs_its_executor() -> None:
    async def fake_executor(
        tool_call_id: str, arguments: Mapping[str, JSONValue]
    ) -> AgentToolResult:
        path = arguments["path"]
        assert isinstance(path, str)
        return AgentToolResult(tool_call_id=tool_call_id, name="read", content=path)

    tool = AgentTool(
        name="read",
        description="Read a file from disk",
        input_schema={"type": "object", "properties": {"path": {"type": "string"}}},
        executor=fake_executor,
    )

    result = asyncio.run(tool.execute("call-1", {"path": "README.md"}))

    assert tool.input_schema["type"] == "object"
    assert tool.description == "Read a file from disk"
    assert result == AgentToolResult(tool_call_id="call-1", name="read", content="README.md")
