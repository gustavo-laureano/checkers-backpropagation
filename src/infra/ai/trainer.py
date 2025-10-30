import torch
import torch.nn as nn
import torch.optim as optim
import random
import matplotlib.pyplot as plt
from typing import List, Tuple
from collections import deque

from src.app.use_cases.game_manager import GameManager
from src.core.board import Board
from src.core.piece import Player
from src.infra.ai.model import CheckersNet, board_to_tensor

# --- CONSTANTES DE TREINAMENTO ---
NUM_EPOCHS = 500             # Quantas "eras" de treinamento
GAMES_PER_EPOCH = 100        # Quantos jogos de autojogo por era
BATCH_SIZE = 64              # Quantas posições treinar de uma vez
LEARNING_RATE = 0.001        # Taxa de aprendizado (o 'passo' do Gradiente Descendente)
MODEL_SAVE_PATH = "checkers_model_v1.pth" # Onde salvar o cérebro treinado

# Parâmetros de Exploração (Epsilon-Greedy)
EPSILON_START = 1.0          # 100% de chance de jogada aleatória no início
EPSILON_END = 0.05           # 5% de chance de jogada aleatória no final
EPSILON_DECAY = 0.99         # Como o epsilon diminui a cada era


@torch.no_grad() # 
def get_best_move_from_model(model: CheckersNet, board: Board, 
                             legal_moves: List[dict], player: Player) -> dict:
    """
    Simula 1 passo à frente para todos os movimentos legais e 
    retorna o movimento que leva ao *menor* score do oponente.
    """
    if not legal_moves:
        return None

    best_score = -float('inf')
    best_move = None
    
    opponent = Player.BLACK if player == Player.WHITE else Player.WHITE

    for move in legal_moves:
        # Simula o movimento
        temp_board = board.deep_copy()
        
        # (Lógica simplificada de 'make_move' para simulação)
        piece = temp_board.get_piece(move["from_pos"][0], move["from_pos"][1])
        temp_board.move_piece(move["from_pos"][0], move["from_pos"][1], 
                              move["to_pos"][0], move["to_pos"][1])
        for cap_pos in move["captures"]:
            temp_board.remove_piece(cap_pos[0], cap_pos[1])
        # (Simplificado: não estamos simulando a promoção aqui, mas poderíamos)

        # Avalia a posição resultante do *ponto de vista do oponente*
        board_tensor = board_to_tensor(temp_board, opponent)
        score_tensor = model(board_tensor)
        score = score_tensor.item()
        
        # Queremos o movimento que MINIMIZA o score do oponente.
        # Minimizar 'score' é o mesmo que maximizar '-score'.
        current_move_score = -score 
        
        if current_move_score > best_score:
            best_score = current_move_score
            best_move = move
            
    return best_move if best_move else random.choice(legal_moves)


# --- FUNÇÃO DE AUTOJOGO (SELF-PLAY) ---

def play_one_game(model: CheckersNet, epsilon: float) -> List[Tuple[Board, Player, float]]:
    """
    Simula um jogo completo de autojogo (IA vs IA).
    Usa Epsilon-Greedy: 'epsilon' de chance de jogar aleatório (Explorar)
    e (1-epsilon) de chance de usar o modelo (Explorar).
    
    Retorna a "memória" do jogo: 
    [(board, player_que_jogou, resultado_final_para_aquele_player), ...]
    """
    
    game = GameManager()
    game_memory: List[Tuple[Board, Player]] = [] # (board_state, player_who_moved)
    
    while not game.get_winner():
        current_player = game.get_current_player()
        legal_moves = game.get_legal_moves()
        
        # Guarda o estado ANTES do movimento
        game_memory.append((game.get_board().deep_copy(), current_player))
        
        # Lógica Epsilon-Greedy
        if random.random() < epsilon:
            # EXPLORAR: Joga aleatoriamente
            chosen_move = random.choice(legal_moves)
        else:
            # EXPLORAR (Exploit): Usa o modelo para escolher a melhor jogada
            chosen_move = get_best_move_from_model(model, game.get_board(), 
                                                   legal_moves, current_player)
        
        game.make_move(chosen_move)

    # O jogo acabou. Descobre o resultado.
    winner = game.get_winner()
    # +1 para vitória, -1 para derrota (vamos ignorar empates por simplicidade)
    
    labeled_data = []
    if winner:
        for board_state, player in game_memory:
            # Se o jogador daquele turno foi o vencedor, seu 'score' é +1
            # Se ele foi o perdedor, seu 'score' é -1
            result = 1.0 if player == winner else -1.0
            labeled_data.append((board_state, player, result))
            
    return labeled_data


# --- O LOOP DE TREINAMENTO PRINCIPAL ---

def train():
    print("--- Iniciando Treinamento da IA ---")
    
    # 1. Carrega o Cérebro e as Ferramentas de Treinamento
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Usando dispositivo: {device}")
    
    model = CheckersNet().to(device)
    
    # Tenta carregar um modelo existente para continuar o treino
    try:
        model.load_state_dict(torch.load(MODEL_SAVE_PATH))
        print(f"Modelo {MODEL_SAVE_PATH} carregado. Continuando treinamento.")
    except FileNotFoundError:
        print(f"Nenhum modelo encontrado. Começando um novo treinamento.")
        
    # Otimizador (Gradiente Descendente) [cite: 13, 21]
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    # Função de Custo (Loss Function) 
    # Queremos que o score (ex: 0.7) chegue perto do resultado (ex: 1.0)
    loss_function = nn.MSELoss() # Mean Squared Error (Erro Quadrático Médio)

    # Guarda o histórico de erros para o gráfico 
    all_epochs_loss = []
    epsilon = EPSILON_START
    
    # "Memória de Longo Prazo" das posições
    replay_memory = deque(maxlen=50000) 

    # 2. O Loop de Treinamento (Eras)
    for epoch in range(NUM_EPOCHS):
        print(f"\n--- ERA {epoch + 1} / {NUM_EPOCHS} ---")
        print(f"Epsilon (Exploração) atual: {epsilon:.4f}")
        
        # --- FASE 1: AUTOJOGO (Coleta de Dados) ---
        # "O treinamento ocorreu por repetição, em milhares de partidas de autojogo" 
        model.eval() # Modo de avaliação (não aprende)
        
        games_played = 0
        while games_played < GAMES_PER_EPOCH:
            game_data = play_one_game(model, epsilon)
            if game_data:
                replay_memory.extend(game_data)
                games_played += 1
                
        if len(replay_memory) < BATCH_SIZE:
            print("Coletando mais dados antes de iniciar o treino...")
            continue
        
        print(f"Jogos simulados. {len(replay_memory)} posições na memória.")

        # --- FASE 2: APRENDIZADO (Backpropagation) ---
        # "demonstrar com clareza o processo de otimização" 
        model.train() # Modo de treinamento (aprende)
        
        epoch_loss = 0.0
        
        # Pega um "lote" aleatório da memória para treinar
        training_batch = random.sample(replay_memory, 
                                     min(len(replay_memory), BATCH_SIZE * 10))
        
        for board_state, player, target_score in training_batch:
            
            # --- O Coração do Aprendizado ---
            
            # 1. Zera os gradientes antigos
            optimizer.zero_grad()
            
            # 2. Converte o estado para Tensor
            tensor = board_to_tensor(board_state, player).to(device)
            target = torch.tensor([target_score], dtype=torch.float32).to(device)
            
            # 3. Forward Pass: Pede a previsão do modelo
            prediction = model(tensor)
            
            # 4. Calcula o "Erro" (Função de Custo) 
            loss = loss_function(prediction, target)
            
            # 5. Backpropagation: Calcula o Gradiente 
            loss.backward()
            
            # 6. Gradiente Descendente: Atualiza os pesos (neurônios) [cite: 13, 21]
            optimizer.step()
            
            epoch_loss += loss.item()
            # --- Fim do Coração ---

        avg_loss = epoch_loss / len(training_batch)
        all_epochs_loss.append(avg_loss)
        print(f"Treinamento da Era concluído. Erro (Loss) médio: {avg_loss:.6f}")
        
        # 3. Salva o Cérebro
        torch.save(model.state_dict(), MODEL_SAVE_PATH)
        
        # 4. Diminui a exploração
        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

    print("\n--- TREINAMENTO CONCLUÍDO ---")
    print(f"Modelo salvo em: {MODEL_SAVE_PATH}")
    
    # 5. Gera o Gráfico da Função de Custo
    # "evidenciada pela redução contínua do erro" 
    plt.figure(figsize=(10, 5))
    plt.plot(all_epochs_loss)
    plt.title("Gráfico de Convergência (Função de Custo vs. Eras)")
    plt.xlabel("Era de Treinamento")
    plt.ylabel("Erro (Loss) Médio")
    plt.grid(True)
    plt.show()


# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    train()