from __future__ import annotations

from collections import Counter
from collections.abc import Collection
from typing import Any


def most_common_element(collection: Collection, *, ignore_none: bool) -> Any | None:
    counter = Counter(filter(None, collection) if ignore_none else collection)
    count = counter.most_common(1)
    return count[0][0] if count else None
