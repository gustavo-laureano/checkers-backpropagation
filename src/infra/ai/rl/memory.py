import random
from collections import deque, namedtuple
from typing import List

# uma única "experiência" de aprendizado.
Transition = namedtuple('Transition', 
                        ('state', 'action', 'next_state', 'reward', 'done'))

class ReplayBuffer:
    def __init__(self, capacity: int = 20000):
        """
        capacity: Número máximo de jogadas que a memória guarda.
                  Quando cheia, remove as mais antigas (FIFO).
        """
        self.memory = deque(maxlen=capacity)

    def push(self, *args):
        """
        Salva uma transição na memória.
        Uso: memory.push(state, action, next_state, reward, done)
        """
        self.memory.append(Transition(*args))

    def sample(self, batch_size: int) -> List[Transition]:
        """
        Retorna um lote (batch) aleatório de experiências para treino.
        É aqui que ocorre a mágica de 'quebrar a correlação'.
        """
        return random.sample(self.memory, batch_size)

    def __len__(self):
        """Retorna quantas experiências temos armazenadas."""
        return len(self.memory)

    def clear(self):
        self.memory.clear()