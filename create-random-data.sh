#!/bin/bash
# Source: https://unix.stackexchange.com/a/199912
seq -w 1 150 | xargs -n1 -I% sh -c 'dd if=/dev/urandom of=/mnt/file.% count=$(shuf -i1-10 -n1) bs=3M'
