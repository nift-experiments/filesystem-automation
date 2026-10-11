#!/usr/bin/env bash
set -euo pipefail
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git build-essential libffi-dev unzip python3-pip strace linux-tools-generic
mkdir -p /opt/filesystem
cd /opt/filesystem
git clone https://github.com/nift-experiments/filesystem-automation.git suite
cd suite
git checkout --detach "$1"
bash scripts/install.sh
python3 scripts/run.py > work/campaign.log 2>&1
python3 scripts/audit.py work/official > work/audit.log 2>&1
bash scripts/cloud-diagnostics.sh > work/diagnostics.log 2>&1
