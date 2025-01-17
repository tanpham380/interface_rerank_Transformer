#!/usr/bin/env bash

set -eou pipefail

docker build --build-arg "MODEL_NAME=$model_name" -t "$local_repo" -f custom.Dockerfile .
