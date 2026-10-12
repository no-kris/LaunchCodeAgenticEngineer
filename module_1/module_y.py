"""
Formatting and reporting utilities for the parallel agent-session example.

This module is intentionally correct but lightly documented. It is designed for
the "Session B" agent task: improve docstrings in this file and update README.md,
without modifying any test files.
"""

from __future__ import annotations


def format_currency(amount: float) -> str:
    """Format a number as a US-dollar string with thousands separators.

    Negative amounts get a leading minus sign before the dollar sign.

    Args:
        amount: The monetary value to format.

    Returns:
        The amount rounded to two decimal places, e.g. ``"$1,234.50"`` or
        ``"-$12.00"``.
    """
    if amount < 0:
        return f"-${abs(amount):,.2f}"
    return f"${amount:,.2f}"


def build_report_title(project_name: str, version: str) -> str:
    """Build a report title in the form ``"<project> — <version>"``.

    Internal whitespace in the project name is collapsed to single spaces and
    both inputs are stripped. Blank values fall back to defaults.

    Args:
        project_name: Name of the project. Defaults to ``"Untitled Project"``
            if blank.
        version: Version label. Defaults to ``"draft"`` if blank.

    Returns:
        The title, joined with an em dash.
    """
    clean_project = " ".join(project_name.strip().split())
    clean_version = version.strip()

    if not clean_project:
        clean_project = "Untitled Project"
    if not clean_version:
        clean_version = "draft"

    return f"{clean_project} — {clean_version}"


def mask_email(email: str) -> str:
    """Mask the local part of an email address for display.

    The first and last characters of the local part are kept and the rest are
    replaced with ``*``. Local parts of one or two characters are masked as
    ``"*"`` and ``"<first>*"`` respectively. The domain is lowercased.

    Args:
        email: The email address to mask. Surrounding whitespace is ignored.

    Returns:
        The masked address, e.g. ``"j**n@example.com"`` for ``"john@Example.com"``.

    Raises:
        ValueError: If the address has no ``@``, or the local part or domain
            is empty.
    """
    email = email.strip()
    if "@" not in email:
        raise ValueError("email must contain @")

    local_part, domain = email.split("@", 1)
    if not local_part or not domain:
        raise ValueError("email must include a local part and domain")

    if len(local_part) == 1:
        masked_local = "*"
    elif len(local_part) == 2:
        masked_local = local_part[0] + "*"
    else:
        masked_local = local_part[0] + "*" * (len(local_part) - 2) + local_part[-1]

    return f"{masked_local}@{domain.lower()}"


def generate_summary_line(name: str, status: str, score: int) -> str:
    """Build a one-line summary in the form ``"<Name>: <status> (<score>)"``.

    The name is whitespace-collapsed and title-cased (``"Unknown"`` if blank).
    The status is stripped, lowercased, and has underscores replaced with
    spaces.

    Args:
        name: Display name of the subject.
        status: Status label, e.g. ``"IN_PROGRESS"``.
        score: Score shown in parentheses.

    Returns:
        The formatted summary line, e.g. ``"Ada Lovelace: in progress (92)"``.
    """
    display_name = " ".join(name.strip().split()).title()
    display_status = status.strip().lower().replace("_", " ")

    if not display_name:
        display_name = "Unknown"

    return f"{display_name}: {display_status} ({score})"


def create_markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    """Render a list of dicts as a Markdown table.

    Columns appear in the order given. A row missing a column renders an empty
    cell; keys not listed in ``columns`` are ignored. Values are converted with
    ``str()`` and are not escaped.

    Args:
        rows: Table rows, each mapping column name to cell value.
        columns: Column names to include, used as the header row.

    Returns:
        The table as a newline-separated string (header, separator, then one
        line per row).

    Raises:
        ValueError: If ``columns`` is empty.
    """
    if not columns:
        raise ValueError("columns cannot be empty")

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"

    body_lines = []
    for row in rows:
        values = [str(row.get(column, "")) for column in columns]
        body_lines.append("| " + " | ".join(values) + " |")

    return "\n".join([header, separator, *body_lines])


def truncate_text(text: str, max_length: int = 80) -> str:
    """Collapse whitespace and truncate text to a maximum length.

    Text longer than ``max_length`` is cut, stripped of trailing whitespace,
    and suffixed with ``"..."`` so the result is at most ``max_length``
    characters.

    Args:
        text: The text to clean and truncate.
        max_length: Maximum length of the result, including the ellipsis.
            Must be at least 4.

    Returns:
        The whitespace-normalized text, truncated with ``"..."`` if needed.

    Raises:
        ValueError: If ``max_length`` is less than 4.
    """
    if max_length < 4:
        raise ValueError("max_length must be at least 4")

    clean_text = " ".join(text.strip().split())
    if len(clean_text) <= max_length:
        return clean_text

    return clean_text[: max_length - 3].rstrip() + "..."
