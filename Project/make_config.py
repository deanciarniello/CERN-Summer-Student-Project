# Packages
#=====================================================
import itertools
import time


# Constants
#=====================================================
FILE_NAME_EXTRA = 'test'                                # Addition string for name of config file
THICKNESS = False                                        # Whether or not the config file includes thickness as a parameter


# Sample data for angles, momenta, particles, 
# and surface types
#=====================================================
output = ["thickness_study"]                            # Name of output file (not including path): 'output', 'angle_study', etc
angles = [45]                                           # Incident Angles (0 is normal to plate): 0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35,37.5,40,42.5,45,47.5,50,52.5,55,57.5,60,62.5,65,67.5,70,72.5,75,77.5,80,82.5,85,87.5
momenta = [50]                                          # Incident Momenta (MeV/c): range(10, 510, 10)
particles = ['mu-']                                     # Incident Particle Type: 'e-', 'mu-', 'mu+', 'proton'
surface_types = [0]                                     # Material of Plate: 0 -> Copper, 1 -> Glass, 2 -> Gold Plated Copper
thicknesses = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] # Thickness of plate (mm)


# Define config file name
#=====================================================
thickness = '_thickness' if THICKNESS else ''
file_name = f'config_{FILE_NAME_EXTRA}_{time.strftime("%Y%m%d.%H%M%S")}{thickness}.txt'
file_path = f'config/{file_name}'


# Generate all combinations using itertools.product
# and save to .txt file in config directory
#=====================================================
if THICKNESS:                                           # Case where thickness is a parameter
    for i, (output_, angle, momentum, particle, surface, thickness) in enumerate(itertools.product(output, angles, momenta, particles, surface_types, thicknesses)):
        with open(file_path, "a" if i > 0 else "w") as f:
            f.write(f'{output_}, {angle}, {momentum}, {particle}, {surface}, {thickness}'+'\n')
            
else:                                                   # Case where thickness is NOT a parameter (default thickness: 5mm)
    for i, (output_, angle, momentum, particle, surface) in enumerate(itertools.product(output, angles, momenta, particles, surface_types)):
        with open(file_path, "a" if i > 0 else "w") as f:
            f.write(f'{output_}, {angle}, {momentum}, {particle}, {surface}'+'\n')

