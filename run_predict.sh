#! /bin/bash

SEED=8

export PYTHONPATH="$PWD" && \
python scripts/training/trainer.py predict \
  --config configurations/large$SEED.yaml \
  --ckpt_path /ceph/inrehbei/proj/srl-test/lightning_logs/spkatt_large-no-bio_seed8/checkpoints/epoch\=18-f1\=0.8322.ckpt



