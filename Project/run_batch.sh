#!/bin/bash

# File: run_batch.sh
# Author: Dean Ciarniello
# Date: 2023-08-08

# Output Directory
# ===========================================
OUTPUT_DIR=/eos/user/d/dciarnie/Data/


# Source gcc and geant4 versions
# ===========================================
echo "start source"
source /cvmfs/sft.cern.ch/lcg/contrib/gcc/10.3.0/x86_64-centos7/setup.sh
source /cvmfs/geant4.cern.ch/geant4/10.7.ref09/x86_64-centos7-gcc10-optdeb/CMake-setup.sh
echo "end source"


# Use user CERNBOX as EOS instance
# ===========================================
echo "start export"
export EOS_MGM_URL=root://eosuser.cern.ch
echo "end export"


# Define the momentum, angle, particle, and material
# ===========================================
output=$1
angle=$2
momentum=$3
particle=$4
material=$5


# Make output directory
# ===========================================
echo "start make output dir"
if [ ! -d "${output}" ]; then
  mkdir -p "${output}"
fi
echo "end make output dir"


# Run Script
# ===========================================
if [ $# -eq 5 ]; then
  # Run script without plate thickness argument
  echo "Running Script"
  ./simulation run.mac $material $angle $momentum $particle output_${material}_${particle}_${momentum}_${angle}.root ${output}/ 0
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

if [ $# -eq 6 ]; then
  # Define thickness
  thickness=$6

  # Run script with plate thickness argument
  echo "Running Script (with thickness arg)"
  ./simulation run.mac $material $angle $momentum $particle output_${material}_${particle}_${momentum}_${angle}_${thickness}.root ${output}/ 0 $thickness
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




