from typing import List, Dict, Any, Tuple, Set
from app.models.review_comment import ReviewComment
from app.models.review_response import ReviewResponse

SEVERITY_ORDER = {
    "INFO": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
}


def _normalize_severity(sev: str) -> str:
    sev = (sev or "").upper()
    return sev if sev in SEVERITY_ORDER else "INFO"


def aggregate_comments(all_comments_raw: List[Dict[str, Any]]) -> ReviewResponse:
    """
    Normalize, deduplicate and sort comments.
    - Deduplicate by (file, line, category)
    - Keep highest severity when duplicates
    - Sort by severity desc, then file, then line
    """

    normalized: List[ReviewComment] = []

    for c in all_comments_raw:
        try:
            comment = ReviewComment(
                file=c.get("file") or "UNKNOWN",
                line=c.get("line"),
                severity=_normalize_severity(c.get("severity", "INFO")),
                category=(c.get("category") or "GENERAL").upper(),
                comment=c.get("comment") or "",
                suggestion=c.get("suggestion"),
            )
            normalized.append(comment)
        except Exception:
            # Skip malformed entries
            continue

    # Deduplicate
    best_by_key: Dict[Tuple[str, int, str], ReviewComment] = {}
    for c in normalized:
        key = (c.file, c.line or -1, c.category)
        if key not in best_by_key:
            best_by_key[key] = c
        else:
            existing = best_by_key[key]
            if SEVERITY_ORDER[c.severity] > SEVERITY_ORDER[existing.severity]:
                best_by_key[key] = c

    deduped = list(best_by_key.values())

    deduped.sort(
        key=lambda c: (-SEVERITY_ORDER[c.severity], c.file, c.line or -1)
    )

    files_touched: Set[str] = {c.file for c in deduped}
    if deduped:
        summary = f"Found {len(deduped)} potential issue(s) across {len(files_touched)} file(s)."
    else:
        summary = "No significant issues found in the changed code."

    return ReviewResponse(summary=summary, comments=deduped)
