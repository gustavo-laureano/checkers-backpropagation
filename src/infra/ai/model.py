import torch
import torch.nn as nn
import torch.nn.functional as F
from src.core.board import Board
from src.core.piece import Player

class CheckersNet(nn.Module):
    """
    Define a arquitetura da Rede Neural (o "cérebro").
    Ela recebe um tabuleiro (como 4x8x8) e retorna um 
    único número (score) entre -1 e 1.
    """
    def __init__(self):
        super(CheckersNet, self).__init__()
        # Input (N, 4, 8, 8) -> (N, 16, 6, 6)
        self.conv1 = nn.Conv2d(4, 16, kernel_size=3, padding=0)
        # (N, 16, 6, 6) -> (N, 32, 4, 4)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=0)
        
        # O tamanho linear será 32 * 4 * 4 = 512
        self.fc1 = nn.Linear(512, 128) # Camada densa 1
        self.fc2 = nn.Linear(128, 1)    # Camada de saída (o "score")

    def forward(self, x):
        # Aplica convolução + ReLU
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        
        # "Achata" o tensor para a camada linear
        x = x.view(-1, 512) 
        
        x = F.relu(self.fc1(x))
        
        # Saída final: usa 'tanh' para garantir que o score
        # fique entre -1 (vitória das Pretas) e +1 (vitória das Brancas).
        x = torch.tanh(self.fc2(x))
        
        return x

def board_to_tensor(board: Board, player: Player) -> torch.Tensor:
    """
    Converte um objeto Board em um Tensor 4x8x8 para a Rede Neural.
    A representação é "centrada no jogador":
    - Canal 0: Peças do jogador atual
    - Canal 1: Damas (Reis) do jogador atual
    - Canal 2: Peças do oponente
    - Canal 3: Damas (Reis) do oponente
    """
    # Cria 4 "planos" 8x8
    player_pieces = torch.zeros((8, 8), dtype=torch.float32)
    player_kings = torch.zeros((8, 8), dtype=torch.float32)
    opponent_pieces = torch.zeros((8, 8), dtype=torch.float32)
    opponent_kings = torch.zeros((8, 8), dtype=torch.float32)

    opponent = Player.BLACK if player == Player.WHITE else Player.WHITE

    for r in range(board.ROWS):
        for c in range(board.COLS):
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
                        
    # Empilha os 4 planos para criar o tensor (4, 8, 8)
    tensor = torch.stack([player_pieces, player_kings, opponent_pieces, opponent_kings])
    # Adiciona a dimensão "batch" (N=1) -> (1, 4, 8, 8)
    tensor = tensor.unsqueeze(0) 
    return tensor