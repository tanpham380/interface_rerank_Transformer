#!/usr/bin/env bash

set -eou pipefail

docker build -t "$LOCAL_REPO" -f custom.Dockerfile .