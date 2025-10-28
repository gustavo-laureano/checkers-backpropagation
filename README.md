# Jogo da Dama com Inteligência Artificial e Cálculo Diferencial e Integral

Este projeto de extensão da Universidade do Estado de Minas Gerais (UEMG) busca desmistificar a ideia de que a Inteligência Artificial (IA) é algo distante e inacessível. Utilizamos a gamificação para demonstrar, de forma prática, como uma IA funciona.

O objetivo central é uma aplicação interativa do Jogo de Damas onde um usuário joga contra uma IA em tempo real. Mais do que um jogo, o projeto exemplifica conceitos de redes neurais e mostra como o cálculo diferencial e o gradiente são fundamentais no processo de aprendizado da IA.

## 🎯 Objetivos Pedagógicos
- Desmistificar a IA: transformar conceitos matemáticos abstratos em uma experiência prática e visível.
- Visualizar o Cálculo: demonstrar como o Gradiente Descendente e o Backpropagation permitem que a IA aprenda e otimize sua tomada de decisão.
- Inspirar e Engajar: mostrar que o desenvolvimento dessa tecnologia é tangível e motivar futuros desenvolvedores.

## 🛠️ Tecnologias Utilizadas
- Linguagem: Python
- Interface Gráfica: Pygame
- Inteligência Artificial: Rede neural implementada com Backpropagation e Gradiente Descendente
- Arquitetura: Clean Architecture (Core, App, Infra)
- Ambiente: Docker e VS Code Dev Containers

## 🚀 Começando

Este repositório foi projetado para rodar dentro de containers Docker, garantindo um ambiente de desenvolvimento consistente.

### Pré-requisitos
- Docker Desktop
- Visual Studio Code
- Extensão Dev Containers para VS Code

### 1. Ambiente de Desenvolvimento (Recomendado)
A forma mais fácil de contribuir é usando o Dev Container.

Clone o repositório e abra a pasta do projeto:
```bash
git clone [https://github.com/gustavo-laureano/checkers-backpropagation.git]
cd projeto-damas-ia
```

Abra a pasta no VS Code. O VS Code detectará a pasta `.devcontainer` e perguntará se deseja "Reabrir no Container". Clique em "Reopen in Container" para iniciar o ambiente.

Para rodar a aplicação de dentro do container (terminal do VS Code):
```bash
python src/infra/main.py
```

### 2. Ambiente de Produção (Execução)
Para construir e rodar a versão final da aplicação (sem as ferramentas de desenvolvimento):

Construir a imagem Docker:
```bash
docker build -t damas-ia:latest .
```

Exemplo de execução no Linux (encaminhar X11):
```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  damas-ia:latest
```

Exemplo para macOS (com XQuartz):
1. No XQuartz, habilite "Allow connections from network clients".
2. Obtenha o IP do host (ex.: `ifconfig en0 | grep inet | awk '$1=="inet" {print $2}'`).
3. Execute:
```bash
docker run -it --rm -e DISPLAY=[SEU_IP_AQUI]:0 damas-ia:latest
```

## 🏛️ Instituição
Universidade do Estado de Minas Gerais – UEMG

## 👥 Autores e Orientadora
- Diego Antonio de Melo Morais (diego.241162951@discente.uemg.br)  
- Gustavo Laureano de Almeida (gustavo.24116622@discente.uemg.br)  
- João Pedro Ferreira Lemos Martins (joao.241167154@discente.uemg.br)  
- Paulo Oliveira Santos (paulo.241167974@discente.uemg.br)

### 👩‍🏫 Orientadora
- Karoliny Danielle Santos (karolliny.santos@uemg.br)

Palavras-chave: Cálculo diferencial e integral; Inteligência Artificial; Jogo da Dama.