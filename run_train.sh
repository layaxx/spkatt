#! /bin/bash

SEED=8

export PYTHONPATH="$PWD" && \
python scripts/training/trainer.py fit \
  --config configurations/large$SEED.yaml &>log.train.spkatt.large.seed$SEED.txt



