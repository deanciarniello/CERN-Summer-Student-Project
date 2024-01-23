# File: setup.sh
# Author: Dean Ciarniello
# Date: 2023-08-09

#!/bin/bash

# Setup Script (for lxplus)
#=====================================================
echo "beginning setup.sh"

# Source geant4 and gcc
#=====================================================
echo "sourcing geant4 and gcc (compiler)"
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/12.1.0/x86_64-el9-gcc12-opt/setup.sh
source /cvmfs/geant4.cern.ch/geant4/11.1.ref10/x86_64-el9-gcc12-optdeb/CMake-setup.sh

# Setup fresh build directory
#=====================================================
echo "making fresh build directory"
if [ -d "build/" ]; then
    rm -r build/
fi
mkdir build
cd build

# Compile Simulation
#=====================================================
echo "compiling simulation"
cmake3 ..
make
cd ..

echo "done setup.sh"