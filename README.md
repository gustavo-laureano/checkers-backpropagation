# Jogo da Dama com Inteligência Artificial e Cálculo Diferencial e Integral

Este projeto de extensão da Universidade do Estado de Minas Gerais (UEMG) busca desmistificar a ideia de que a Inteligência Artificial (IA) é algo distante e inacessível. Utilizamos a gamificação para demonstrar, de forma prática, como uma IA funciona.

O objetivo central é uma aplicação interativa do Jogo de Damas onde um usuário joga contra uma IA em tempo real. Mais do que um jogo, o projeto exemplifica conceitos de redes neurais e mostra como o cálculo diferencial e o gradiente são fundamentais no processo de aprendizado da IA.

## 🎯 Objetivos Pedagógicos
- **Desmistificar a IA**: transformar conceitos matemáticos abstratos em uma experiência prática e visível.
- **Visualizar o Cálculo**: demonstrar como o Gradiente Descendente e o Backpropagation permitem que a IA aprenda e otimize sua tomada de decisão.
- **Inspirar e Engajar**: mostrar que o desenvolvimento dessa tecnologia é tangível e motivar futuros desenvolvedores.

## 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python 3.11+
- **Interface Gráfica**: Pygame
- **Inteligência Artificial**: Rede neural com Backpropagation e Gradiente Descendente
- **Arquitetura**: Clean Architecture (Core, App, Infra)
- **Ambiente**: Docker e VS Code Dev Containers
- **Testes**: pytest com cobertura de código



## 📖 Documentação Completa

Para instruções detalhadas de instalação, configuração e solução de problemas, consulte:

### **[📘 Guia Completo de Execução](docs/RUNNING.md)**

Este guia inclui:
- ✅ Configuração passo a passo para Linux, macOS e Windows
- ✅ Solução de problemas comuns
- ✅ Configuração de servidores X11
- ✅ Diferentes modos de execução
- ✅ Troubleshooting detalhado

## 🎮 Como Jogar

1. **Clique** em uma peça branca (você joga com as brancas)
2. As casas válidas serão **destacadas em verde**
3. **Clique** na casa de destino para mover
4. **Capturas são obrigatórias** quando disponíveis
5. Peças que chegam ao final do tabuleiro viram **damas** (com coroa 👑)
6. Vença capturando todas as peças adversárias ou deixando-o sem movimentos!


## 🏗️ Arquitetura do Projeto

O projeto segue os princípios da **Clean Architecture**:

### **Core** (Entidades de Domínio)
- [`Board`](src/core/board.py): Representação do tabuleiro 8x8
- [`Piece`](src/core/piece.py): Peças do jogo (normais e damas)
- [`Move`](src/core/move.py): Estrutura de movimentos

### **App** (Casos de Uso)
- [`GameManager`](src/app/use_cases/game_manager.py): Gerencia o fluxo do jogo
- [`MoveValidator`](src/app/use_cases/move_validator.py): Valida movimentos legais
- [`AIInterface`](src/app/interfaces/ai_interface.py): Interface para implementações de IA

### **Infra** (Implementações)
- [`PygameView`](src/infra/ui/pygame_view.py): Interface gráfica com Pygame
- [`NeuralNetPlayer`](src/infra/ai/neural_net_player.py): Jogador IA (em desenvolvimento)
- [`Trainer`](src/infra/ai/trainer.py): Sistema de treinamento (em desenvolvimento)


## 🔬 Próximos Passos

- [ ] Implementação completa da rede neural
- [ ] Sistema de treinamento por autojogo (self-play)
- [ ] Visualização do processo de backpropagation
- [ ] Interface para acompanhar o aprendizado da IA
- [ ] Sistema de replay de partidas
- [ ] Diferentes níveis de dificuldade

## 🤝 Como Contribuir

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é parte de um projeto de extensão acadêmica da UEMG.

## 🏛️ Instituição

**Universidade do Estado de Minas Gerais – UEMG**

## 👥 Equipe

### Desenvolvedores
- **Diego Antonio de Melo Morais** - [diego.241162951@discente.uemg.br](mailto:diego.241162951@discente.uemg.br)
- **Gustavo Laureano de Almeida** - [gustavo.24116622@discente.uemg.br](mailto:gustavo.24116622@discente.uemg.br)
- **João Pedro Ferreira Lemos Martins** - [joao.241167154@discente.uemg.br](mailto:joao.241167154@discente.uemg.br)
- **Paulo Oliveira Santos** - [paulo.241167974@discente.uemg.br](mailto:paulo.241167974@discente.uemg.br)

### Orientadora
- **Profa. Karoliny Danielle Santos** - [karolliny.santos@uemg.br](mailto:karolliny.santos@uemg.br)

## 🔗 Links Úteis

- [Documentação do Pygame](https://www.pygame.org/docs/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Backpropagation Explained](https://www.youtube.com/watch?v=Ilg3gGewQ5U)
- [Docker Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

## 📊 Status do Projeto

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Pygame](https://img.shields.io/badge/pygame-2.5.0+-green)
![License](https://img.shields.io/badge/license-Academic-orange)

---

**Palavras-chave**: Cálculo diferencial e integral · Inteligência Artificial · Jogo da Dama · Backpropagation · Redes Neurais · Gamificação

**Atualizado em 29-10-2025 por @gustavo_laureano**