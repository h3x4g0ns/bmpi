# MLP

**MLP** is a webserver for servicing ML models for inferencing.

## How it works

Models are defined in `models/*` in PyTorch.

We define the config for serving these models in `config.py`.

The Flask api at `api.py` is responsible for serving the models and implements a GPU model cache from `cache.py`.

## To Do

- [ ] add a training script for custom models
- [ ] add whisper
- [ ] add object detection
- [ ] implement muli-gpu scheduling
