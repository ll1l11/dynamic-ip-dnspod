#!/usr/bin/env bash
export LC_ALL="en_US.UTF-8"
LOG_PATH="push-ip.log"
cd "$( dirname "${BASH_SOURCE[0]}" )"

touch ip.txt >> $LOG_PATH 2>&1

if [ $? -ne 0 ]
then
    echo "touch ip.txt error" | tee -a $LOG_PATH
    exit 1
fi

$(which ifconfig) | awk '$1=="inet" {print $2}' | grep -v '127.0.0.1' | sed 's/addr://g' > ip.txt
# 如果有多个网卡， 将对应网卡作为参数，例如
# $(which ifconfig) eth0 | awk '$1=="inet" {print $2}' | grep -v '127.0.0.1' | sed 's/addr://g' > ip.txt
# get public ip # dig +short myip.opendns.com @resolver1.opendns.com > "$CURDIR/ip.txt"

source "/home/ubuntu/.virtualenvs/py3/bin/activate" >> $LOG_PATH 2>&1  && python set_record.py 2>&1 | tee -a $LOG_PATH
