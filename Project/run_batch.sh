#!/bin/bash

# File: run_batch.sh
# Author: Dean Ciarniello
# Date: 2023-08-08

# Output Directory
# ===========================================
OUTPUT_DIR=/eos/user/d/dciarnie/Data/


# Use user CERNBOX as EOS instance
# ===========================================
echo "start export"
export EOS_MGM_URL=root://eosuser.cern.ch
echo "end export"


# Source gcc and geant4 versions
# ===========================================
echo "start source"
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/12.1.0/x86_64-el9-gcc12-opt/setup.sh
source /cvmfs/geant4.cern.ch/geant4/11.1.ref10/x86_64-el9-gcc12-optdeb/CMake-setup.sh
echo "end source"


# Define the momentum, angle, particle, material, and mac file
# ===========================================
output=$1
angle=$2
momentum=$3
particle=$4
material=$5
mac=$6

# Make output directory
# ===========================================
echo "start make output dir"
if [ ! -d "${output}" ]; then
  mkdir -p "${output}"
fi
echo "end make output dir"


# Run Script
# ===========================================
if [ $# -eq 6 ]; then
  # Run script without plate thickness argument
  echo "Running Script"
  ./simulation $mac $material $angle $momentum $particle output_${material}_${particle}_${momentum}_${angle}.root ${output}/ 0
  echo "Finished Script"

  # For staging out a directory
  # ===========================================
  echo "Moving Files from ${output} to EOS"
  eos cp -r ${output}/output_${material}_${particle}_${momentum}_${angle}.root ${OUTPUT_DIR}${output}
  echo "Done Moving Files to EOS"

  echo "Removing output from EOS"
  rm -r ${output}
  echo "Done removing output from EOS"
fi

if [ $# -eq 7 ]; then
  # Define thickness
  thickness=$7

  # Run script with plate thickness argument
  echo "Running Script (with thickness arg)"
  ./simulation $mac $material $angle $momentum $particle output_${material}_${particle}_${momentum}_${angle}_${thickness}.root ${output}/ 0 $thickness
  echo "Finished Script (with thickness arg)"

  # For staging out a directory
  # ===========================================
  echo "Moving Files from ${output} to EOS"
  eos cp -r ${output}/output_${material}_${particle}_${momentum}_${angle}_${thickness}.root ${OUTPUT_DIR}${output}
  echo "Done Moving Files to EOS"

  echo "Removing output from EOS"
  rm -r ${output}
  echo "Done removing output from EOS"
fi




