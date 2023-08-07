#!/bin/bash
echo "beginning setup.sh"

# source geant4 and gcc
echo "sourcing geant4 and gcc (compiler)"
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/10.3.0/x86_64-centos7/setup.sh
source /cvmfs/geant4.cern.ch/geant4/10.7.ref09/x86_64-centos7-gcc10-optdeb/CMake-setup.sh

# Setup fresh build directory
echo "making fresh build directory"
if [ -d "build/" ]; then
    rm -r build/
fi
mkdir build
cd build

# Compile Simulation
echo "compiling simulation"
cmake3 ..
make
cd ..

echo "done setup.sh"