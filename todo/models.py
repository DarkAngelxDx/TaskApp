from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"  # low | medium | high
    deadline: Optional[str] = None  # YYYY-MM-DD
    done: bool = False
