# Packages
# ======================================================
import numpy as np
import matplotlib.pyplot as plt
import uproot

# Number of Events
# ======================================================
EVENTS=100000

# Simulation Configurations
# Note: data files for all permutations must be 
#       present in the specified directory
# ======================================================
MOMENTUM = 50                   # Momentum in MeV/c
ANGLE = 45                      # Angle in degrees: 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70, 72.5, 75, 77.5, 80, 82.5, 85, 87.5
SURFACE = 0                     # Surface (0->Copper; 1->Glass; 2->Gold-Plated Copper): 0, 1, 2
PARTICLE = "mu-"                # Particle Type: "mu-", "e-", "proton", "mu+"
THICKNESSES = range(5,105,5)    # Range of thicknesses for study (mm)

# Data Directory
# Info: directory where the data files are located
# ======================================================
DATA = "/eos/user/d/dciarnie/Data/thickness_study/"


# =Helper Functions
# ======================================================
def return_surface_name(surface):
    '''
        Parameters:
            surface (int):                  0 (Copper); 1 (Glass); 2 (Gold-Plated Copper)
        
        Returns:
            surface_name (string):          name of corresponding surface/material
    '''
    surface_name = ""
    if surface == 0:
        surface_name = "Copper"
    if surface == 1:
        surface_name = "Glass"
    if surface == 2:
        surface_name = "Gold-Plated-Copper"
    return surface_name


# ========== Main Code ==========
n_reflected = []    # number of reflected particles in each configuration

# Iterate over all thicknesses in THICKNESSES
for thickness_index, thickness in enumerate(THICKNESSES):
    path = DATA + 'output_'+str(SURFACE)+'_'+str(PARTICLE)+'_'+str(MOMENTUM)+'_'+str(ANGLE)+'_'+str(thickness)+'.root'
    #print(path)
    with uproot.open(path) as file:
        theta = file["PrimaryEvents"]["fTheta"]     # Theta of non-absorbed/decayed particles (just used to determine number of reflected particles)
        theta = np.asarray(theta)                   
        theta = theta[theta <= 90]                  # Cut out transmitted events
        n_reflected.append(len(theta))              # Append the number of reflected events for configuration to n_reflected
    
# Make scatter plot of number of reflected events vs thickness of scattering plate
fig, ax = plt.subplots()
ax.scatter(THICKNESSES, n_reflected, marker='o', edgecolors='black')
ax.set_xlabel("Thickness (mm)", fontsize=9, fontweight='bold')
ax.set_ylabel("N Reflected", fontsize=9, fontweight='bold')
ax.set_title(f"Thickness Study\n Particle: {PARTICLE}, Surface: {return_surface_name(SURFACE)}, Momentum: {MOMENTUM} MeV/c, Angle: {ANGLE} deg\nN Events = {EVENTS}", fontsize=11)
ax.grid(True, linestyle='--', linewidth=0.5)
ax.tick_params(axis='both', which='major', labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim([0, 1.1*max(THICKNESSES)])
ax.set_ylim([0, 1.5*max(n_reflected)])
fig.tight_layout(pad=2)
fig.savefig(f'thickness_study_{return_surface_name(SURFACE)}_{PARTICLE}_{MOMENTUM}_{ANGLE}.png')
plt.close()