import torch
import torch.nn as nn
import torch.nn.functional as F
from src.core.board import Board
from src.core.piece import Player

class CheckersNet(nn.Module):
    """
    Arquitetura da Rede Neural com MÁSCARA DE EFICIÊNCIA.
    """
    def __init__(self):
        super(CheckersNet, self).__init__()
        
        # --- CAMADAS CONVOLUCIONAIS ---
        # Input (N, 4, 8, 8) -> (N, 16, 6, 6)
        self.conv1 = nn.Conv2d(4, 16, kernel_size=3, padding=0)
        # (N, 16, 6, 6) -> (N, 32, 4, 4)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=0)
        
        # --- CAMADAS DENSAS ---
        self.fc1 = nn.Linear(32 * 4 * 4, 128) 
        self.fc2 = nn.Linear(128, 1)

        # --- OTIMIZAÇÃO: MÁSCARA ESTÁTICA ---
        # Criamos uma máscara que tem 1 nas casas pretas e 0 nas brancas.
        # "register_buffer" diz ao PyTorch: "Isso faz parte do modelo, mas NÃO treine isso (não é peso)"
        mask = torch.zeros((1, 1, 8, 8))
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 == 1: # Casas pretas (válidas)
                    mask[0, 0, r, c] = 1.0
        self.register_buffer('valid_squares_mask', mask)

    def forward(self, x):
        # 1. APLICAR MÁSCARA (HARD ATTENTION)
        # Multiplicamos a entrada pela máscara.
        # Tudo que for casa branca vira ZERO instantaneamente.
        # Isso impede que "ruído" nas casas brancas passe para as camadas seguintes.
        x = x * self.valid_squares_mask
        
        # 2. Convoluções
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        
        # 3. Flatten & Dense
        x = x.view(-1, 32 * 4 * 4) 
        x = F.relu(self.fc1(x))
        
        # 4. Saída Tanh (-1 a 1)
        x = torch.tanh(self.fc2(x))
        
        return x

def board_to_tensor(board: Board, player: Player) -> torch.Tensor:
    """
    Converte Board -> Tensor Otimizado
    """
    # Cria 4 "planos" 8x8
    player_pieces = torch.zeros((8, 8), dtype=torch.float32)
    player_kings = torch.zeros((8, 8), dtype=torch.float32)
    opponent_pieces = torch.zeros((8, 8), dtype=torch.float32)
    opponent_kings = torch.zeros((8, 8), dtype=torch.float32)

    opponent = Player.BLACK if player == Player.WHITE else Player.WHITE

    # Iteração Otimizada: Se tiver como iterar só casas válidas no Board seria melhor,
    # mas aqui mantemos o loop simples e a Rede Neural cuida de filtrar o lixo.
    for r in range(board.ROWS):
        for c in range(board.COLS):
            # Otimização de CPU: Se for casa branca, nem acessa a memória da peça
            if (r + c) % 2 == 0:
                continue

            piece = board.get_piece(r, c)
            if piece:
                if piece.player == player:
                    player_pieces[r, c] = 1
                    if piece.is_king:
                        player_kings[r, c] = 1
                elif piece.player == opponent:
                    opponent_pieces[r, c] = 1
                    if piece.is_king:
                        opponent_kings[r, c] = 1
                        
    tensor = torch.stack([player_pieces, player_kings, opponent_pieces, opponent_kings])
    tensor = tensor.unsqueeze(0) 
    return tensor