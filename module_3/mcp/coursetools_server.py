"""Dummy MCP server for the scoped-agent orchestration lesson.

This server is a safe stand-in for course tools. It exposes the tools named in the
lesson and enforces a role-based allow-list loaded from mcp/roles.allowlist.json.

Each tool expects a ``role`` argument so students can verify that denied calls fail
with an authorization error. The server is deliberately small and should be used
only for local course exercises.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

SERVER_NAME = "coursetools"
mcp = FastMCP(SERVER_NAME)

ROOT = Path(os.environ.get("COURSETOOLS_ROOT", ".")).resolve()
ALLOWLIST_PATH = Path(os.environ.get("COURSETOOLS_ALLOWLIST", "mcp/roles.allowlist.json"))

DEFAULT_ALLOWLIST: dict[str, list[str]] = {
    "file_read": ["planner", "implementer", "reviewer", "tester", "orchestrator"],
    "file_write": ["implementer", "orchestrator"],
    "codebase_search": ["planner", "implementer", "reviewer"],
    "shell": [],
    "test_runner": ["tester"],
    "task_tracker": ["project-manager"],
    "web_search": ["researcher"],
}


def load_allowlist() -> dict[str, list[str]]:
    if ALLOWLIST_PATH.exists():
        return json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    return DEFAULT_ALLOWLIST


ALLOWLIST = load_allowlist()


def authorize(tool_name: str, role: str) -> None:
    allowed_roles = ALLOWLIST.get(tool_name, [])
    if role not in allowed_roles:
        raise PermissionError(
            f"Authorization error: role '{role}' is not on the allow-list for {tool_name}. "
            f"Allowed roles: {allowed_roles or 'none'}."
        )


def safe_path(path: str) -> Path:
    candidate = (ROOT / path).resolve()
    if not str(candidate).startswith(str(ROOT)):
        raise ValueError(f"Path escapes the project root: {path}")
    return candidate


@mcp.tool()
def file_read(role: str, path: str) -> str:
    """Read a UTF-8 text file from the project root."""
    authorize("file_read", role)
    target = safe_path(path)
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(path)
    return target.read_text(encoding="utf-8")


@mcp.tool()
def file_write(role: str, path: str, content: str) -> str:
    """Write a UTF-8 text file under the project root."""
    authorize("file_write", role)
    target = safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Wrote {path} ({len(content)} bytes)."


@mcp.tool()
def codebase_search(role: str, query: str, root: str = ".", max_results: int = 20) -> list[dict[str, Any]]:
    """Search text files under the project root for a query string."""
    authorize("codebase_search", role)
    search_root = safe_path(root)
    results: list[dict[str, Any]] = []
    ignored_dirs = {".git", "node_modules", ".venv", "__pycache__"}

    for path in search_root.rglob("*"):
        if len(results) >= max_results:
            break
        if any(part in ignored_dirs for part in path.parts):
            continue
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        line_matches = []
        for number, line in enumerate(text.splitlines(), start=1):
            if query.lower() in line.lower():
                line_matches.append({"line": number, "text": line.strip()})
                if len(line_matches) >= 3:
                    break
        if line_matches:
            results.append({"path": str(path.relative_to(ROOT)), "matches": line_matches})
    return results


@mcp.tool()
def shell(role: str, command: str) -> str:
    """Simulate a shell command. This dummy server does not execute arbitrary commands."""
    authorize("shell", role)
    return f"Simulated shell command only; nothing executed: {command}"


TEST_TIMEOUT_SECONDS = int(os.environ.get("COURSETOOLS_TEST_TIMEOUT", "300"))
MAX_OUTPUT_CHARS = 20000


def _run_fixed(cmd: list[str], cwd: Path) -> tuple[int, str]:
    """Run one fixed, allow-listed command (no shell) and return (exit code, output)."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=TEST_TIMEOUT_SECONDS,
            env={**os.environ, "CI": "1", "FORCE_COLOR": "0"},
        )
    except subprocess.TimeoutExpired:
        return 124, f"Timed out after {TEST_TIMEOUT_SECONDS}s: {' '.join(cmd)}"
    except FileNotFoundError as exc:
        return 127, f"Command not found: {exc}"
    output = (proc.stdout or "") + (proc.stderr or "")
    if len(output) > MAX_OUTPUT_CHARS:
        output = "...[truncated]...\n" + output[-MAX_OUTPUT_CHARS:]
    return proc.returncode, output


@mcp.tool()
def test_runner(role: str, path: str = ".", suite: str = "default", install: bool = True) -> str:
    """Run a Node project's real test suite: `npm install` (if requested) then `npm test`.

    `path` is the project directory (relative to the project root) containing
    package.json. Only these two fixed commands are executed; no arbitrary shell
    input is accepted. `suite` is accepted for backward compatibility and ignored.
    Returns exit codes and the real command output.
    """
    authorize("test_runner", role)
    project_dir = safe_path(path)
    if not (project_dir / "package.json").is_file():
        raise FileNotFoundError(f"No package.json in {path}")

    report: list[str] = [f"Project: {path}"]
    if install:
        code, out = _run_fixed(["npm", "install", "--no-audit", "--no-fund"], project_dir)
        report.append(f"== npm install (exit {code}) ==\n{out}")
        if code != 0:
            report.append("RESULT: ERROR (install failed; tests not run)")
            return "\n".join(report)

    code, out = _run_fixed(["npm", "test"], project_dir)
    report.append(f"== npm test (exit {code}) ==\n{out}")
    report.append(f"RESULT: {'PASS' if code == 0 else 'FAIL'} (npm test exit code {code})")
    return "\n".join(report)


@mcp.tool()
def task_tracker(role: str, ticket_id: str, status: str = "done", note: str = "") -> str:
    """Simulate updating a shared work ticket."""
    authorize("task_tracker", role)
    return f"Ticket {ticket_id} updated to {status}. Note: {note or 'No note provided.'}"


@mcp.tool()
def web_search(role: str, question: str) -> dict[str, Any]:
    """Return a deterministic, example research answer for course exercises."""
    authorize("web_search", role)
    return {
        "answer": "For CSV output, double quotes inside a field should be escaped by doubling them, and fields containing commas, quotes, or line breaks should be wrapped in double quotes.",
        "key_facts": [
            "Use comma-separated headers and rows.",
            "Quote fields containing commas, quotes, or newlines.",
            "Escape embedded double quotes as two double quotes.",
        ],
        "sources": [
            "RFC 4180 common CSV format conventions",
            "Spreadsheet-compatible CSV escaping behavior",
        ],
        "question": question,
    }


if __name__ == "__main__":
    mcp.run()
