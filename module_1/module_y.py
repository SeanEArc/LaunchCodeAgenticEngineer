"""
Formatting and reporting utilities for the parallel agent-session example.

This module is intentionally correct but lightly documented. It is designed for
the "Session B" agent task: improve docstrings in this file and update README.md,
without modifying any test files.
"""

from __future__ import annotations


def format_currency(amount: float) -> str:
    """Return an amount formatted as US dollars with thousands separators.

    Negative amounts place the sign before the dollar symbol, so ``-1234.5``
    becomes ``-$1,234.50`` rather than ``$-1,234.50``.
    """
    if amount < 0:
        return f"-${abs(amount):,.2f}"
    return f"${amount:,.2f}"


def build_report_title(project_name: str, version: str) -> str:
    """Return a report title combining a project name and version.

    Surrounding and repeated whitespace is collapsed in both parts. A blank
    project name falls back to ``"Untitled Project"`` and a blank version falls
    back to ``"draft"``, so the result is never partially empty.
    """
    clean_project = " ".join(project_name.strip().split())
    clean_version = version.strip()

    if not clean_project:
        clean_project = "Untitled Project"
    if not clean_version:
        clean_version = "draft"

    return f"{clean_project} — {clean_version}"


def mask_email(email: str) -> str:
    """Return an email address with its local part obscured for display.

    The first and last characters of the local part are kept and the rest are
    replaced with asterisks; a one-character local part becomes ``"*"`` and a
    two-character one keeps only its first character. The domain is lowercased.

    Raises:
        ValueError: If the address has no ``@``, or is missing a local part or
            a domain.
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
    """Return a one-line ``"Name: status (score)"`` summary for a record.

    The name is whitespace-collapsed and title-cased, falling back to
    ``"Unknown"`` when blank. The status is lowercased and underscores become
    spaces, so ``"IN_PROGRESS"`` renders as ``"in progress"``.
    """
    display_name = " ".join(name.strip().split()).title()
    display_status = status.strip().lower().replace("_", " ")

    if not display_name:
        display_name = "Unknown"

    return f"{display_name}: {display_status} ({score})"


def create_markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    """Return a Markdown table built from ``rows`` using ``columns`` as headers.

    Each column name is looked up as a key in every row, and values are
    stringified. A row missing a key renders as an empty cell, and an empty
    ``rows`` list yields a header and separator with no body.

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
    """Return text collapsed to single spaces and shortened to ``max_length``.

    Text that already fits is returned unchanged apart from whitespace
    collapsing. Longer text is cut and suffixed with ``"..."``, and the returned
    string never exceeds ``max_length`` because the ellipsis is counted within
    the budget.

    Raises:
        ValueError: If ``max_length`` is less than 4, which leaves no room for
            content alongside the ellipsis.
    """
    if max_length < 4:
        raise ValueError("max_length must be at least 4")

    clean_text = " ".join(text.strip().split())
    if len(clean_text) <= max_length:
        return clean_text

    return clean_text[: max_length - 3].rstrip() + "..."
