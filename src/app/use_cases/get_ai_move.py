from ..interfaces.ai_interface import AIInterface


def get_ai_move(ai: AIInterface, board_state):
    """Call the AI interface to get the next move."""
    return ai.get_best_move(board_state)
