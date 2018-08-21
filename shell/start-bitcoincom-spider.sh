#!/usr/bin/env bash

SCRIPT=`readlink -f "$0"`
SHELL_DIR=`dirname "$SCRIPT"`
DIR=`dirname "$SHELL_DIR"`

SOURCE='bitcoincom'

cd $DIR
mkdir -p .docker

## Fetch interval from arguments
test -z $1 && PARAM='1' || PARAM=$1
test "$PARAM" -lt '60' && PARAM='60'
PARAM="$PARAM""s"

docker run -d --rm --name "scheduled-$SOURCE""-spider-$PARAM" -v "$(pwd)/.docker/":/out crypto-trading-volume-spider:latest python /app/$SOURCE.py $@
