# 🚀 Guia de Execução

Este documento fornece instruções detalhadas para executar o Jogo de Damas com IA em diferentes ambientes.

## 📋 Pré-requisitos

### Para Desenvolvimento (Dev Container)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Extensão Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Para Execução Direta (Produção)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Servidor X11 (para exibição gráfica):
  - **Linux**: Já incluído no sistema
  - **macOS**: [XQuartz](https://www.xquartz.org/)
  - **Windows**: [VcXsrv](https://sourceforge.net/projects/vcxsrv/) ou [Xming](http://www.straightrunning.com/XmingNotes/)

---

## 🛠️ Modo 1: Desenvolvimento com Dev Container (Recomendado)

Este é o método mais simples para desenvolver e testar o projeto.

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/gustavo-laureano/checkers-backpropagation.git
cd checkers-backpropagation
```

### Passo 2: Abra no VS Code

```bash
code .
```

### Passo 3: Reabra no Container

1. O VS Code detectará automaticamente o arquivo [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json)
2. Clique em **"Reopen in Container"** no popup que aparecer
3. Aguarde a construção do container (primeira vez pode demorar alguns minutos)

### Passo 4: Instale o visualizador

1. Instale e inicie o [VcXsrv](https://sourceforge.net/projects/vcxsrv/) ou Xming
2. Configure o servidor X:
   - Display number: 0
   - Start no client
   - Disable access control: **marcado**

### Passo 5: Execute o Jogo

No VS Code abra um novo terminal bash (dentro do container).
Garanta que está na \workspace e execute o seguinte comando para iniciar a execução:

```bash
python -m src.infra.main
```

### Problemas Comuns - Dev Container

#### ❌ Erro: "Display not available"

**Solução para Linux:**
```bash
# No terminal do HOST (fora do container)
xhost +local:docker
```

**Solução para macOS:**
1. Abra o XQuartz
2. Vá em Preferências → Security
3. Marque "Allow connections from network clients"
4. Execute no terminal do HOST:
```bash
export IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
xhost + $IP
```

**Solução para Windows:**
1. Abra o VcXsrv com as opções:
   - Multiple windows
   - Display number: 0
   - Disable access control: **marcado**
2. Configure a variável de ambiente no [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json):
```json
"containerEnv": {
  "DISPLAY": "host.docker.internal:0.0"
}
```

---

## 🐳 Modo 2: Execução com Docker (Produção)

### Passo 1: Construa a Imagem

```bash
docker build -t checkers-ai:latest .
```

### Passo 2: Configure o Servidor X11

#### **Linux**

```bash
# Permita conexões locais do Docker
xhost +local:docker
```

#### **macOS**

1. Instale e inicie o XQuartz:
```bash
brew install --cask xquartz
open -a XQuartz
```

2. Configure as preferências do XQuartz:
   - XQuartz → Preferências → Security
   - Marque "Allow connections from network clients"

3. Obtenha o IP do host:
```bash
export IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
echo $IP
```

4. Permita conexões:
```bash
xhost + $IP
```

#### **Windows**

1. Instale e inicie o VcXsrv ou Xming
2. Configure o servidor X:
   - Display number: 0
   - Start no client
   - Disable access control: **marcado**

### Passo 3: Execute o Container

#### **Linux**

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  checkers-ai:latest
```

#### **macOS**

```bash
# Substitua SEU_IP_AQUI pelo IP obtido anteriormente
docker run -it --rm \
  -e DISPLAY=SEU_IP_AQUI:0 \
  checkers-ai:latest
```

Exemplo:
```bash
docker run -it --rm \
  -e DISPLAY=192.168.1.100:0 \
  checkers-ai:latest
```

#### **Windows (PowerShell)**

```powershell
docker run -it --rm `
  -e DISPLAY=host.docker.internal:0.0 `
  checkers-ai:latest
```

---

## 🧪 Modo 3: Execução Local (Sem Docker)

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/gustavo-laureano/checkers-backpropagation.git
cd checkers-backpropagation
```

### Passo 2: Instale as Dependências

#### **Linux (Ubuntu/Debian)**

```bash
# Instale as bibliotecas SDL2
sudo apt-get update
sudo apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    python3-pip

# Instale as dependências Python
pip3 install -r requirements.txt
```

#### **macOS**

```bash
# Instale as bibliotecas SDL2
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf

# Instale as dependências Python
pip3 install -r requirements.txt
```

#### **Windows**

1. Baixe o instalador do Python 3.11+ do [site oficial](https://www.python.org/downloads/)
2. Durante a instalação, marque "Add Python to PATH"
3. Abra o PowerShell e execute:

```powershell
pip install -r requirements.txt
```

### Passo 3: Execute o Jogo

```bash
python src/infra/main.py
```

---

## ⚙️ Usando o Makefile

O projeto inclui um [`Makefile`](Makefile) com comandos úteis:

```bash
# Instalar dependências
make install

# Executar o jogo
make run

# Executar testes
make test

# Formatar código
make format

# Executar linter
make lint

# Limpar arquivos temporários
make clean
```

---

## 🎮 Como Jogar

1. **Seleção de Peça**: Clique em uma peça branca (você joga com as brancas)
2. **Movimentos Destacados**: As casas válidas ficarão destacadas em verde
3. **Executar Movimento**: Clique na casa de destino desejada
4. **Capturas**: Capturas são obrigatórias quando disponíveis
5. **Damas**: Peças promovidas a damas têm uma coroa
6. **Vitória**: O jogo termina quando um jogador não tem mais movimentos

---

## 🐛 Troubleshooting

### Problema: Tela preta ou janela não abre

**Solução:**
1. Verifique se o servidor X11 está rodando
2. Teste a variável DISPLAY:
```bash
echo $DISPLAY
```
3. Reinicie o servidor X11

### Problema: Erro "pygame.error: No available video device"

**Solução para Docker:**
```bash
# Adicione --privileged ao comando docker run
docker run -it --rm --privileged \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  checkers-ai:latest
```

### Problema: Permissão negada ao acessar /tmp/.X11-unix

**Solução (Linux):**
```bash
xhost +local:docker
# Ou, mais seguro:
xhost +local:$(docker inspect --format='{{ .Config.Hostname }}' CONTAINER_ID)
```

### Problema: ModuleNotFoundError

**Solução:**
```bash
# Certifique-se de estar no diretório raiz do projeto
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python src/infra/main.py
```

---

## 📚 Recursos Adicionais

- [Documentação do Pygame](https://www.pygame.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Dev Containers Tutorial](https://code.visualstudio.com/docs/devcontainers/tutorial)
- [XQuartz FAQ](https://www.xquartz.org/FAQ.html)

---

## 🆘 Suporte

Se você encontrar problemas não listados aqui:

1. Verifique as [Issues no GitHub](https://github.com/gustavo-laureano/checkers-backpropagation/issues)
2. Abra uma nova issue com:
   - Sistema operacional
   - Versão do Docker
   - Mensagem de erro completa
   - Passos para reproduzir o problema

---

**Atualizado em 29-10-2025 por @gustavo-laureano**