#!/usr/bin/env bash

SCRIPT=`readlink -f "$0"`
DIR=`dirname "$SCRIPT"`
cd $DIR

rm -f ./python/*.pyc
docker build . -t crypto-trading-volume-spider:latest
