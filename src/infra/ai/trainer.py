import torch
import torch.nn as nn
import torch.optim as optim
import random
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
from collections import deque
from datetime import datetime
import os
from itertools import count

from src.app.use_cases.game_manager import GameManager
from src.core.board import Board
from src.core.piece import Player
from src.infra.ai.model import CheckersNet, board_to_tensor

# --- CONSTANTES PADRÃO (Podem ser sobrescritas na classe) ---
BATCH_SIZE = 64
GAMMA = 0.99
EPS_START = 1.0
EPS_END = 0.05
EPS_DECAY = 1000  # Decaimento mais suave
TARGET_UPDATE = 10
LEARNING_RATE = 1e-4
MEMORY_SIZE = 10000
NUM_EPISODES = 50000
MODEL_BASE_NAME = "checkers_model"

class CheckersTrainer:
    def __init__(self, load_existing: bool = True):
        # 1. Configuração de Hardware e Caminhos
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"--- CheckersTrainer inicializado em: {self.device} ---")
        
        self.load_path, self.save_path = self._find_model_paths()
        
        # 2. Redes Neurais (Policy = Jogador, Target = Gabarito Estável)
        self.policy_net = CheckersNet().to(self.device)
        self.target_net = CheckersNet().to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval() # Target nunca treina, só é atualizada
        
        # 3. Carregamento de Modelo Existente
        if load_existing and self.load_path:
            try:
                self.policy_net.load_state_dict(torch.load(self.load_path, map_location=self.device))
                self.target_net.load_state_dict(self.policy_net.state_dict())
                print(f"Modelo carregado: {self.load_path}")
            except Exception as e:
                print(f"Erro ao carregar modelo: {e}. Iniciando do zero.")
        
        print(f"O treinamento salvará em: {self.save_path}")

        # 4. Ferramentas de Aprendizado
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=LEARNING_RATE)
        self.memory = deque(maxlen=MEMORY_SIZE)
        self.loss_function = nn.SmoothL1Loss() # Melhor que MSE para RL (menos sensível a erros explosivos)

        # 5. Estado do Treinamento
        self.steps_done = 0
        self.loss_history = []

    def _find_model_paths(self) -> Tuple[Optional[str], str]:
        """Gerencia versões do arquivo automaticamente (v1 -> v2 -> v3)"""
        version = 1
        load_path = None
        while True:
            current = f"{MODEL_BASE_NAME}_v{version}.pth"
            if not os.path.exists(current):
                save_path = current
                if version > 1:
                    load_path = f"{MODEL_BASE_NAME}_v{version - 1}.pth"
                break
            version += 1
        return load_path, save_path

    def get_epsilon(self) -> float:
        """Retorna o valor atual de epsilon (taxa de exploração)"""
        eps_threshold = EPS_END + (EPS_START - EPS_END) * \
            (1.0 / (1.0 + self.steps_done / EPS_DECAY))
        return eps_threshold

    def select_action(self, state_tensor, legal_moves, game_manager: GameManager):
        """Escolhe ação baseada em Epsilon-Greedy com Simulação de Futuro"""
        sample = random.random()
        # Fórmula de decaimento exponencial do epsilon
        eps_threshold = self.get_epsilon()
        self.steps_done += 1

        # A. Exploração (Aleatório)
        if sample < eps_threshold:
            return random.choice(legal_moves)
        
        # B. Exploração (Inteligência da Rede)
        with torch.no_grad():
            best_score = -float('inf')
            best_move = None
            current_player = game_manager.get_current_player()
            
            for move in legal_moves:
                # Simula o futuro sem estragar o jogo atual
                future_board = game_manager.simulate_move(move)
                
                # Avalia para o jogador atual
                future_tensor = board_to_tensor(future_board, current_player).to(self.device)
                score = self.policy_net(future_tensor).item()
                
                if score > best_score:
                    best_score = score
                    best_move = move
            
            return best_move if best_move else random.choice(legal_moves)

    def optimize_model(self):
        """O coração do aprendizado: Backpropagation com Replay Buffer"""
        if len(self.memory) < BATCH_SIZE:
            return 0.0

        # Amostra um lote aleatório da memória
        transitions = random.sample(self.memory, BATCH_SIZE)
        
        # Transforma lista de tuplas em tupla de listas
        batch_state, batch_action_idx, batch_next_state, batch_reward = zip(*transitions)
        
        state_batch = torch.cat(batch_state)
        reward_batch = torch.cat(batch_reward)
        
        # Filtra estados finais (que não têm next_state)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch_next_state)), 
                                      device=self.device, dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch_next_state if s is not None])

        # 1. Previsão da Rede (Q-Values atuais)
        # Nota simplificada: Nossa rede avalia estados, não pares estado-ação diretamente.
        # Usamos o valor do estado como proxy.
        state_values = self.policy_net(state_batch)

        # 2. Valor Esperado (Pela Target Network)
        next_state_values = torch.zeros(BATCH_SIZE, device=self.device)
        next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()
        
        # Fórmula de Bellman: Q_new = Reward + Gamma * Q_next
        expected_state_values = (next_state_values * GAMMA) + reward_batch

        # 3. Calcula Perda e Otimiza
        loss = self.loss_function(state_values, expected_state_values.unsqueeze(1))
        
        self.optimizer.zero_grad()
        loss.backward()
        
        # Gradient Clipping (Evita explosão de gradientes - Fase 2.4 do Roteiro)
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
            
        self.optimizer.step()
        
        return loss.item()

    def train(self):
        print(f"--- Iniciando Treinamento ({NUM_EPISODES} episódios) ---")
        
        for i_episode in range(NUM_EPISODES):
            game = GameManager()
            current_board = game.get_board()
            current_player = game.get_current_player()
            
            # Estado Inicial
            state = board_to_tensor(current_board, current_player).to(self.device)
            total_loss = 0
            steps = 0
            
            # Loop do Jogo
            for t in count():
                legal_moves = game.get_legal_moves()
                if not legal_moves:
                    break 
                
                # Escolhe e Executa Ação
                action = self.select_action(state, legal_moves, game)
                
                # Precisamos de uma cópia para calcular recompensa baseada na diferença
                # (Por enquanto usaremos recompensa simples de vitória/derrota no final para não complicar,
                #  mas a estrutura para rewards.py está pronta para ser plugada aqui)
                game.make_move(action)
                
                winner = game.get_winner()
                reward_val = 0.0
                done = False

                if winner:
                    reward_val = 1.0 if winner == current_player else -1.0
                    done = True
                
                reward = torch.tensor([reward_val], device=self.device)
                
                # Define Próximo Estado
                if done:
                    next_state = None
                else:
                    next_state = board_to_tensor(game.get_board(), game.get_current_player()).to(self.device)

                # Salva na Memória
                # (Simplificação: não estamos salvando a ação específica, pois nossa rede avalia estados.
                #  Para DQN puro precisaríamos indexar a ação. Mantemos simples por enquanto.)
                self.memory.append((state, 0, next_state, reward))
                
                state = next_state

                # Otimiza
                loss = self.optimize_model()
                total_loss += loss
                steps += 1
                
                if done:
                    break

            # Fim do Episódio
            if i_episode % TARGET_UPDATE == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())
            
            avg_loss = total_loss / steps if steps > 0 else 0
            self.loss_history.append(avg_loss)
            
            print(f"Episódio {i_episode+1}/{NUM_EPISODES} | Steps: {steps} | Loss: {avg_loss:.5f}")
            
            # Salva Checkpoint periodicamente
            if (i_episode + 1) % 50 == 0:
                torch.save(self.policy_net.state_dict(), self.save_path)

        print("--- Treinamento Concluído ---")
        self._plot_results()

    def _plot_results(self):
        if not os.path.exists("graphs"):
            os.makedirs("graphs")
        plt.figure(figsize=(10, 5))
        plt.plot(self.loss_history)
        plt.title("Evolução do Erro (Loss) por Episódio")
        plt.xlabel("Episódio")
        plt.ylabel("Loss Médio")
        plt.grid(True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
        plt.savefig(f"graphs/treino_{timestamp}.png")
        print(f"Gráfico salvo em graphs/treino_{timestamp}.png")

if __name__ == "__main__":
    trainer = CheckersTrainer()
    trainer.train()