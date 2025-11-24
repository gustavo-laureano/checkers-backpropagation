from src.core.board import Board
from src.core.piece import Player
from src.app.use_cases.move_validator import Move

# Valores definidos no seu Roteiro (Fase 2.3)
REWARD_WIN = 1.0
REWARD_LOSS = -1.0
REWARD_PROMOTION = 0.5   # Virar Dama
REWARD_CAPTURE = 0.1     # Comer peça
REWARD_DEFAULT = 0.0     # Movimento comum

def calculate_reward(
    board_before: Board, 
    board_after: Board, 
    move: Move, 
    player: Player, 
    winner: Player | None
) -> float:
    """
    Calcula a recompensa imediata para uma ação tomada.
    Isso ajuda a IA a aprender passos intermediários antes de saber dar xeque-mate.
    """
    
    # 1. Recompensa Máxima: Vitória/Derrota
    if winner:
        if winner == player:
            return REWARD_WIN
        else:
            return REWARD_LOSS

    # Se o jogo não acabou, calculamos recompensas parciais
    total_reward = REWARD_DEFAULT

    # 2. Recompensa por Captura (Material)
    # O objeto Move já nos diz quantas capturas ocorreram nessa jogada
    if move and "captures" in move:
        num_captures = len(move["captures"])
        total_reward += (num_captures * REWARD_CAPTURE)

    # 3. Recompensa por Promoção (Estratégia)
    # Verificamos se a peça que moveu virou Dama
    # A peça está agora na posição final (to_pos)
    to_r, to_c = move["to_pos"]
    piece_after = board_after.get_piece(to_r, to_c)
    
    # Precisamos saber se ela JÁ ERA dama antes. 
    # Olhamos a posição de origem no board antigo.
    from_r, from_c = move["from_pos"]
    piece_before = board_before.get_piece(from_r, from_c)

    if piece_after and piece_before:
        # Se ela não era rei antes, mas é agora = Promoção aconteceu
        if not piece_before.is_king and piece_after.is_king:
            total_reward += REWARD_PROMOTION

    return total_reward