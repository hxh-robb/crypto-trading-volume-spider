#!/usr/bin/env bash

SCRIPT=`readlink -f "$0"`
DIR=`dirname "$SCRIPT"`
cd $DIR
mkdir -p .docker

test -z $1 && PARAM='1' || PARAM=$1
PARAM="$PARAM""s"

#docker build . -t coinmarketcap-spider:latest
docker run -d --rm --name "coinmarketcap-spider-$PARAM" -v "$(pwd)/.docker/":/out coinmarketcap-spider:latest python /app/app.py $@
