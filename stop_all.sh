#!/usr/bin/zsh

sudo fuser -k 5432/tcp ; \
sudo fuser -k 6379/tcp ; \
sudo sysctl vm.overcommit_memory=1 ; \
