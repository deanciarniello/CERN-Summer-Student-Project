# File: analysis_depth.py
# Author: Dean Ciarniello
# Date: 2024-01-23

# Packages
# ======================================================
import numpy as np
import matplotlib.pyplot as plt
import uproot
import sys
import os

from analysis_helpers import return_surface_name

# Number of Events
# ======================================================
EVENTS = 100000

# Simulation Configurations
# Note: data files for all permutations must be 
#       present in the specified directory
# ======================================================
MOMENTUM = 140                   # Momentum in MeV/c
MATERIAL = 3                    # Material (0->Copper; 1->Glass; 2->Gold-Plated Copper): 0, 1, 2
PARTICLE = "mu-"                # Particle Type: "mu-", "e-", "proton", "mu+"
ANGLES = np.arange(0, 90, 2.5)       # Range of angles for study
THICKNESS = 30                  # 30mm thickness for depth studies

# Data Directory
# Info: directory where the data files are located
# ======================================================
DATA = "/eos/user/d/dciarnie/Data/mu-_depth_study_30mm/"

PLOTS = "./depth_plots/"


# ========== Main Code ==========
n_reflected = []    # number of reflected particles in each configuration
max_depths = []     # maximum depth for each incident angle
mean_depths = []
depths_list = []    # list to store depths for each incident angle
angles_to_plot = []


fig1, ax1 = plt.subplots()


# Iterate over all thicknesses in THICKNESSES
for angle_index, angle in enumerate(ANGLES):
        # Record path to specific data files
    path1 = DATA + "output_" +str(MATERIAL)+'_'+str(PARTICLE)+'_'+str(MOMENTUM)+'_'+str(angle)+'.root'
    path2 = DATA + "output_" +str(MATERIAL)+'_'+str(PARTICLE)+'_'+str(MOMENTUM)+'_'+str(angle)+'_'+str(THICKNESS)+'.root'
    path3 = DATA + "output_" +str(MATERIAL)+'_'+str(PARTICLE)+'_'+str(MOMENTUM)+'_'+str(round(angle))+'.root'
    path4 = DATA + "output_" +str(MATERIAL)+'_'+str(PARTICLE)+'_'+str(MOMENTUM)+'_'+str(round(angle))+'_'+str(THICKNESS)+'.root'
    if os.path.exists(path1):
        path = path1
    elif os.path.exists(path2):
        path=path2
    elif os.path.exists(path3):
        path=path3
    elif os.path.exists(path4):
        path=path4
    else:
        print(" ********** NO FILE FOUND ********** ")
        print(path1)
        print(path2)
        print(path3)
        print(path4)
        sys.exit(1)
                    
    with uproot.open(path) as file:
        depth = file["PrimaryEvents"]["fDepth"]
        depth = np.asarray(depth)
        depth = depth[depth<=THICKNESS]
        depth = depth[depth!=10.000000]
        count_depth = len(depth)
        if count_depth == 0: continue
        max_depth = np.max(depth)
        mean_depth = np.nanmean(depth)
        max_depths.append(max_depth)
        mean_depths.append(mean_depth)
        depths_list.append(depth)
        angles_to_plot.append(angle)
        
        
        if ((angle in (70,82.5,87.5)) and (count_depth > 0)):
            fig2, ax2 = plt.subplots()
            
            # Histogram of depth
            ax2.hist(depth, bins='auto', range=(0, max_depth), histtype='step', color='blue', linewidth=1)
            ax2.set_xlabel("Depth (mm)", fontsize=9, fontweight='bold')
            ax2.set_ylabel("Count", fontsize=9, fontweight='bold')
            ax2.set_title(f"Depth Histogram\n Particle: {PARTICLE}, Surface: {return_surface_name(MATERIAL)}, Momentum: {MOMENTUM} MeV/c\nAngle: {angle} deg, Count: {count_depth}/{EVENTS}", fontsize=11)
            # Grid and tick mark settings
            ax2.grid(True, linestyle='--', linewidth=0.5)
            ax2.tick_params(axis='both', which='major', labelsize=10)
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.yaxis.tick_left()
            
            # Make legend
            #ax2.legend(fontsize=8)
            
            fig2.savefig(PLOTS + f'depth_study_histogram_{PARTICLE}_{return_surface_name(MATERIAL)}_{MOMENTUM}_{angle}.png')
            print("MADE: " + f'depth_study_histogram_{PARTICLE}_{return_surface_name(MATERIAL)}_{MOMENTUM}_{angle}.png')


# Scatter plot
ax1.scatter(angles_to_plot, max_depths, marker='o', edgecolors='black', label="Max Depth")
ax1.scatter(angles_to_plot, mean_depths, marker='o', edgecolors='black', label="Mean Depth")
ax1.set_xlabel("Incident Angle (degrees)", fontsize=9, fontweight='bold')
ax1.set_ylabel("Depth (mm)", fontsize=9, fontweight='bold')
ax1.set_title(f"Depth vs Incident Angle\n Particle: {PARTICLE}, Surface: {return_surface_name(MATERIAL)}, Momentum: {MOMENTUM} MeV/c", fontsize=11)
ax1.grid(True, linestyle='--', linewidth=0.5)
ax1.tick_params(axis='both', which='major', labelsize=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_xlim([0, 90])
ax1.legend(fontsize=8)

# Save and close figure
fig1.tight_layout(pad=2)
fig1.savefig(PLOTS + f'depth_study_scatterplot_{PARTICLE}_{return_surface_name(MATERIAL)}_{MOMENTUM}.png')
