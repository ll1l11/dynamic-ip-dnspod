#!/usr/bin/env bash
export LC_ALL="en_US.UTF-8"
cd "$( dirname "${BASH_SOURCE[0]}" )"

$(which ifconfig) | awk '$1=="inet" {print $2}' | grep -v '127.0.0.1' | sed 's/addr://g' > ip.txt
# get public ip # dig +short myip.opendns.com @resolver1.opendns.com > "$CURDIR/ip.txt"

source "/home/ubuntu/.virtualenvs/py3/bin/activate" && python set_record.py
