import numpy as np
import matplotlib.pyplot as plt
import uproot

EVENTS=100000

MOMENTA = [50]
ANGLES = [45] # 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70, 72.5, 75, 77.5, 80, 82.5, 85, 87.5
SURFACES = [0] # 0, 1, 2
PARTICLES = ["mu-"] #"mu-", "e-", "proton", "mu+"
THICKNESSES = range(5,105,5)

# Root directory where the files are located
DATA = "/eos/user/d/dciarnie/Data/thickness_study/"


# ========== HELPER FUNCTIONS ==========
def return_surface_name(surface):
    surface_name = ""
    if surface == 0:
        surface_name = "Copper"
    if surface == 1:
        surface_name = "Glass"
    if surface == 2:
        surface_name = "Gold-Plated-Copper"
    return surface_name


# ========== Main Code ==========
# Perform Analysis and Make Plots
for particle in PARTICLES:
    for surface in SURFACES:
        for momentum_index, momentum in enumerate(MOMENTA):
            for angle_index, angle in enumerate(ANGLES):
                n_reflected = []
                for thickness_index, thickness in enumerate(THICKNESSES):
                    path = DATA + 'output_'+str(surface)+'_'+str(particle)+'_'+str(momentum)+'_'+str(angle)+'_'+str(thickness)+'.root'
                    print(path)
                    with uproot.open(path) as file:
                        theta = file["PrimaryEvents"]["fTheta"]
                        theta = np.asarray(theta)
                        theta = theta[theta <= 90]  # Cut out transmitted events
                        n_reflected.append(len(theta)) # Number of reflected events for this config (angle, momentum, particle, material)
                    
                fig, ax = plt.subplots()
                ax.scatter(THICKNESSES, n_reflected, marker='o', edgecolors='black')
                ax.set_xlabel("Thickness (mm)", fontsize=9, fontweight='bold')
                ax.set_ylabel("N Reflected", fontsize=9, fontweight='bold')
                ax.set_title(f"Thickness Study\n Particle: {particle}, Surface: {return_surface_name(surface)}, Momentum: {momentum} MeV/c, Angle: {angle} deg\nN Events = {EVENTS}", fontsize=11)
                ax.grid(True, linestyle='--', linewidth=0.5)
                ax.tick_params(axis='both', which='major', labelsize=10)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.set_xlim([0, max(THICKNESSES)+5])
                ax.set_ylim([0, max(n_reflected)+10])
                fig.tight_layout(pad=2)
                fig.savefig(f'thickness_study_{return_surface_name(surface)}_{particle}_{momentum}_{angle}.png')
                plt.close()