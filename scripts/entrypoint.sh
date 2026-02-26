#!/bin/bash
set -e

# Install any custom nodes listed in nodes.toml
/app/venv/bin/python /app/scripts/install_nodes.py

# Start ComfyUI
exec /app/venv/bin/python main.py \
    --listen 0.0.0.0 \
    --port 8188 \
    --disable-auto-launch \
    --highvram \
    --extra-model-paths-config /app/extra_model_paths.yaml
