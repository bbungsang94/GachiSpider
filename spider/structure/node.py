from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Node:
    url: str
    freshness: int = 0
    last_visited: float = None
    cache: object = None
    label: str = None
    data: object = None
    pattern: str = None
    fan_in: List[object] = None
    fan_out: List[object] = None