#! /bin/bash

SEED=42

export PYTHONPATH="$PWD" && \
python scripts/training/trainer.py predict \
  --config configurations/large$SEED.yaml \
  --ckpt_path models/spkatt_large_seed42/checkpoints/epoch\=25-f1\=0.8260.ckpt 



