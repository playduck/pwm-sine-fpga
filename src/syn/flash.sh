#!/bin/bash

BITSTREAM="$(dirname "$0")/out/$1.bit"
ecpdap flash write --freq 100M $BITSTREAM
