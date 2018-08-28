#!/usr/bin/env bash

SCRIPT=`readlink -f "$0"`
SHELL_DIR=`dirname "$SCRIPT"`
DIR=`dirname "$SHELL_DIR"`

cd $DIR
mkdir -p .docker

docker run -d --rm --name "scheduled-cmc-pro-api-spider" -v "$(pwd)/.docker/":/out -v "$(pwd)/.docker/cmc_api_keys.txt":/cmc/api_keys.txt crypto-trading-volume-spider:latest python /app/cmc-pro-api.py
