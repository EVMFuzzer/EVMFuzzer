#!/bin/sh
# generate aleth (if aleth-vm in benchmarkEVMs folder cannot work)
# cd benchmarkEVMs
# git clone --recursive https://github.com/ethereum/aleth.git
# cd aleth
# mkdir build 
# cd build  
# cmake .. -DVMTRACE=ON  # Configure the project.
# cmake --build .        # Build all default targets.
# cd ../..
# cp aleth/build/aleth-vm/aleth-vm .

# geth
sudo apt-get install software-properties-common
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum

# solc
sudo apt-get install solc
