#!/bin/bash

BITSTREAM="$(dirname "$0")/out/$1.bit"
ecpdap program --freq 100M $BITSTREAM
