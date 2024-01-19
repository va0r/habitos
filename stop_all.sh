#!/usr/bin/zsh

while sudo fuser -k 5432/tcp ; do
    echo "Waiting for processes on port 5432 to finish..."
    sleep 1
done ; \

while sudo fuser -k 6379/tcp ; do
    echo "Waiting for processes on port 6379 to finish..."
    sleep 1
done ; \

sudo sysctl vm.overcommit_memory=1 ; \
