#!/bin/bash

# Define the momentum range, angle, particles, and materials
momenta=(seq -w 010 20 050) #20 500
angles=(seq -w 30 1 40) #1 89
particles=("mu+") # "mu-" "e-" "proton"
materials=(0) # 1 2

if [ ! -d "./output/" ]; then
  mkdir -p "./output/"
fi

# Loop over the parameters and run the C++ scripts
for angle in $angles; do
  for particle in "${particles[@]}"; do
    for material in "${materials[@]}"; do
      for momentum in "${momenta[@]}"; do
        if [ ! -d "./output/${material}/" ]; then
          mkdir -p "./output/${material}/"
        fi
        if [ ! -d "./output/${material}/${particle}/" ]; then
          mkdir -p "./output/${material}/${particle}/"
        fi
        if [ ! -d "./output/${material}/${particle}/${angle}/" ]; then
          mkdir -p "./output/${material}/${particle}/${angle}/"
        fi
        if [ ! -d "./output/${material}/${particle}/${angle}/${momentum}/" ]; then
          mkdir -p "./output/${material}/${particle}/${angle}/${momentum}/"
        fi
        ./build/simulation run.mac $material $angle $momentum  $particle output.root ./output/${material}/${particle}/${angle}/${momentum}/ 0
      done
    done
  done
done
