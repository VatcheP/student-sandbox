from datetime import datetime
from typing import Any


def infer_value(value: str) -> Any:
    """Infer a Python type from a CSV string value."""
    text = value.strip()

    if text == "":
        return ""

    lowered = text.lower()

    if lowered == "true":
        return True

    if lowered == "false":
        return False

    try:
        return int(text)
    except ValueError:
        pass

    try:
        return float(text)
    except ValueError:
        pass

    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass

    return text