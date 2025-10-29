from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Move:
    src: Tuple[int, int]
    dst: Tuple[int, int]
    captures: List[Tuple[int, int]] = None

    def is_capture(self) -> bool:
        return bool(self.captures)
