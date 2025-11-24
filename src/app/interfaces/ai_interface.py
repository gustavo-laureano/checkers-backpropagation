from abc import ABC, abstractmethod
from typing import Any


class AIInterface(ABC):
    """Abstract AI interface that concrete AI players must implement."""

    @abstractmethod
    def get_best_move(self, board_state: Any):
        """Return the best move given a board state.

        board_state: an opaque representation (implementation-defined)
        Returns an object representing a Move (could be `src.core.move.Move`).
        """
        raise NotImplementedError
