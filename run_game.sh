#!/bin/bash
cd /workspace

export DISPLAY=host.docker.internal:0.0

PYTHONPATH=/workspace python3 src/infra/main.py
