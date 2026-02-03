#!/usr/bin/env bash
set -euo pipefail

# Ensure repo root is on import path even when executed from subdirectories.
PYTHONPATH=. python -u attack_scenarios/attack_01_epoch_skip/runner.py
