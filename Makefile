.PHONY: help test run clean install format lint

help:
	@echo "Comandos disponíveis:"
	@echo " make install 	- Instala dependências"
	@echo " make test 		- Executa testes"
	@echo " make run 		- Executa o jogo"
	@echo " make format - Formata código com black"
	@echo " make lint 		- Executa pylint"
	@echo " make clean 	- Remove arquivos temporários"

install:
	pip install --no-cache-dir -r requirements.txt

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

run:
	@echo "🎮 Iniciando Jogo de Damas..."
	@DISPLAY=host.docker.internal:0.0 \
	PYTHONPATH=/workspace \
	SDL_AUDIODRIVER=dummy \
	python3 src/infra/main.py 2>&1 | grep -v "ALSA\|XDG_RUNTIME_DIR" || true

format:
	black src/ tests/

lint:
	pylint src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ .coverage htmlcov/