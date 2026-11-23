"""Row-limit helpers for the CSV export module."""

from __future__ import annotations

# Per error-codes.md, E_EXPORT_417 (precondition not met at generation time)
# is the closest documented export code; no dedicated "limit exceeded" code exists.
EXPORT_LIMIT_ERROR_CODE = "E_EXPORT_417"

# Placeholder default: no export row limit was found in the codebase or corpus.
# Confirm the real value with the owner of the export configuration.
MAX_EXPORT_ROWS = 5000


class ExportLimitExceeded(Exception):
    """Raised when an export dataset exceeds the configured row limit."""

    def __init__(self, row_count: int, limit: int, code: str = EXPORT_LIMIT_ERROR_CODE):
        self.row_count = row_count
        self.limit = limit
        self.code = code
        super().__init__(
            f"{code}: export of {row_count} rows exceeds the limit of {limit} rows"
        )


def get_export_row_limit(row_count: int | None = None) -> int:
    """Return the configured max export row limit.

    If ``row_count`` is given and exceeds the limit, raise ExportLimitExceeded.
    The check is a simple count comparison, so it does not load data into memory
    (the export streams rows in batches of 500).
    """
    limit = MAX_EXPORT_ROWS
    if row_count is not None and row_count > limit:
        raise ExportLimitExceeded(row_count, limit)
    return limit
