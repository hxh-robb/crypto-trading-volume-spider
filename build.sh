#!/usr/bin/env bash

SCRIPT=`readlink -f "$0"`
DIR=`dirname "$SCRIPT"`
cd $DIR

docker build . -t coinmarketcap-spider:latest
