#####################################################
#   analysis.py                                     #
#---------------------------------------------------#
#   Details:                                        #
#   Script to read output data from Geant4          #
#   scattering simulation. Options to produce:      #
#       *histograms of reflected angles             #
#       *histograms of reflected momenta            #
#       *correlation 2d histograms of reflected     #
#           angle vs momenta                        #
#       *arrays of histograms for each of the       #
#           above options                           #
#       *scatter plots (with errors) of the mode    #
#           and mean of reflected angle             #
#           distributions                           #
#                                                   #
#---------------------------------------------------#
#   Author: Dean Ciarniello [2023-08-08]            #
#####################################################


# Packages
#=====================================================
import numpy as np
from scipy.stats import *
from scipy import stats, optimize
import scipy as sc
import matplotlib.pyplot as plt
import uproot
import os


# Plotting Options
#=====================================================
ANGLE_HISTOGRAMS = False
MOMENTUM_HISTOGRAMS = False
CORRELATION_HISTOGRAM_ANGLE_MOMENTUM = False
ANGLE_HISTOGRAM_ARRAY = False
MOMENTUM_HISTOGRAM_ARRAY = False
CORRELATION_HISTOGRAM_ANGLE_MOMENTUM_ARRAY = False
ANGLES_SCATTER_PLOT = True
MOMENTUM_SCATTER_PLOT = False
#=====================================================


# Number of Events
#=====================================================
EVENTS=100000
#=====================================================


# Plotting Configuration
# Note: data for any permutations must be in the DATA directory
#=====================================================
MOMENTA = [50, 100, 150, 200]
ANGLES = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70, 72.5, 75, 77.5, 80, 82.5, 85, 87.5] # 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70, 72.5, 75, 77.5, 80, 82.5, 85, 87.5
SURFACES = [0] # 0, 1, 2
PARTICLES = ["e-", "proton", "mu+"] #"mu-", "e-", "proton", "mu+"
#=====================================================


# Data Directory
# Info: directory where the files are located
#=====================================================
DATA = "/eos/user/d/dciarnie/Data/output_mt/output_mt/output/"
#=====================================================



# Helper Functions
#=====================================================
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

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def reduced_chi_squared(observed, expected, errors, dof):
    '''
        Parameters: 
            observed (float array):             observed values
            expected (float array):             expected values
            errors (float array):               errors of observed values
            dof (int):                          degrees of freedom
            
        Returns:
            r_chi_squared (float):
    '''
    r_chi_squared = np.sum(((observed - expected) / errors) ** 2) / dof
    return r_chi_squared

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_angle_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected):
    # Fit to beta distribution and compute reduced chi-squared
    params = stats.beta.fit(thetas, floc=0, fscale=90)
    fitted_pdf = stats.beta.pdf(np.linspace(0, 90, 90), *params)
    observed_counts, _ = np.histogram(thetas, bins=90, range=(0, 90))
    expected_counts = len(thetas) * fitted_pdf
    degrees_of_freedom = len(observed_counts) - len(params)  # Number of bins - number of fit parameters
    reduced_chi2 = reduced_chi_squared(observed_counts[1:-1], expected_counts[1:-1], np.sqrt(expected_counts[1:-1]), degrees_of_freedom)
                       
    # Plot fitted beta distribution 
    ax_h.plot(np.linspace(0, 90, 90), fitted_pdf,'r-', label=f'Fitted Beta Distribution \nParams: [{params[2]:.0f},{params[3]:.0f}], a={params[0]:.2f}, b={params[1]:.2f}\nChi2/dof: {reduced_chi2:.2f}')

    # Plot histogram
    n, bins, _ = ax_h.hist(thetas, bins='scott', range=(0, 90), density=True, histtype='step', color='blue', linewidth=1, label=f"$\sigma: {std_dev_:.2f}$")
    ax_h.axvline(mean_, 0, 1, color='black', linestyle='dashed', linewidth=1, label=f"Mean: {mean_:.2f}")
    ax_h.axvline(mode_, 0, 1, color='green', linestyle='dashed', linewidth=1, label=f"Mode: {mode_:.1f}")
    ax_h.axvline(angle, 0, 1, color='red', linewidth=4, alpha=0.5, label=f"Incident Angle: {angle:.2f}")
    ax_h.set_xlabel("Reflected Angle (deg)", fontsize=10)
    ax_h.set_ylabel("Normalized Rate", fontsize=10)
    ax_h.grid(True, linestyle='--', linewidth=0.5)
    ax_h.tick_params(axis='both', which='major', labelsize=10)
    ax_h.spines['top'].set_visible(False)
    ax_h.spines['right'].set_visible(False)
    ax_h.yaxis.tick_left()
    ax_h.yaxis.set_label_position("left")
    ax_h.legend(fontsize=8)
    
    return [n]

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_angle_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected):
    setup = setup_angle_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected)
    ax_h.set_title(f"Particle: {particle}, Surface: {surface_name}, Momentum: {momentum}MeV/c, Angle: {angle}deg \nEvents: Total={total}, Reflected={reflected}", fontsize=11)
    ax_h.set_ylim([0,1.01*np.max(setup[0])])

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_angle_histogram_a(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected):
    setup = setup_angle_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected)
    ax_h.set_title(f"Momentum: {momentum}MeV/c, Angle: {angle}deg\nN Reflected: {reflected}", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected):
    n, bins, _ = ax_h.hist(momenta, bins='scott', range=(0, momentum), density=True, histtype='step', color='blue', linewidth=1, label=f"$\sigma$: {std_dev_:.2f} MeV/c")
    ax_h.axvline(mean_, 0, 1, color='black', linestyle='dashed', linewidth=1, label=f"Mean: {mean_:.2f} MeV/c ({(mean_/momentum)*100:.2f}% of Incident)")
    ax_h.axvline(mode_, 0, 1, color='green', linestyle='dashed', linewidth=1, label=f"Mode: {mode_:.1f} MeV/c ({(mode_/momentum)*100:.1f}% of Incident)")
    ax_h.axvline(momentum, 0, 1, color='red', linewidth=4, alpha=0.5, label=f"Incident Momentum: {momentum:.2f} MeV/c")
    ax_h.set_xlabel("Reflected Momentum (MeV/c)", fontsize=10)
    ax_h.set_ylabel("Normalized Rate", fontsize=10)
    ax_h.grid(True, linestyle='--', linewidth=0.5)
    ax_h.tick_params(axis='both', which='major', labelsize=10)
    ax_h.spines['top'].set_visible(False)
    ax_h.spines['right'].set_visible(False)
    ax_h.yaxis.tick_left()
    ax_h.yaxis.set_label_position("left")
    ax_h.legend(fontsize=8)
    
    return [n]

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected):
    setup = setup_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected)
    ax_h.set_ylim([0,1.01*np.max(setup[0])])
    ax_h.set_title(f"Particle: {particle}, Surface: {surface_name}, Momentum: {momentum}MeV/c, Angle: {angle}deg \nEvents: Total={total}, Reflected={reflected}", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_momentum_histogram_a(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected):
    setup = setup_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, angle, total, reflected)
    ax_h.set_title(f"Momentum: {momentum}MeV/c, Angle: {angle}deg \nN Reflected={reflected}", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, surface_name, momentum, angle, total, reflected):
    counts_theta, bins_theta = np.histogram(thetas, bins='scott', range=(0,90))
    counts_momentum, bins_momentum = np.histogram(momenta, bins='scott', range=(0,momentum))
    hist = ax_h_cor.hist2d(thetas, momenta, bins=[bins_theta, bins_momentum], cmap='magma')
    ax_h_cor.set_ylabel("Reflected Momentum (MeV/c)", fontsize=10)
    ax_h_cor.set_xlabel("Reflected Angle (deg)", fontsize=10)
    ax_h_cor.set_title(f"Particle: {particle}, Surface: {surface_name}, Momentum: {momentum}MeV/c, Angle: {angle}deg \nEvents: Total={total}, Reflected={reflected}", fontsize=11)
    
    # Add color bar for the intensity scale
    cbar = fig_h_cor.colorbar(hist[3], ax=ax_h_cor)
    cbar.set_label('Count')

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_histogram_a(fig_cor_array, axes_cor_array, thetas, momenta, particle, surface_name, momentum, angle, total, reflected):
    counts_theta, bins_theta = np.histogram(thetas, bins='scott', range=(0,90))
    counts_momentum, bins_momentum = np.histogram(momenta, bins='scott', range=(0,momentum))
    hist = axes_cor_array.hist2d(thetas, momenta, bins=[bins_theta, bins_momentum], density=True, cmap='magma')
    axes_cor_array.set_ylabel("Reflected Momentum (MeV/c)", fontsize=10)
    axes_cor_array.set_xlabel("Reflected Angle (deg)", fontsize=10)
    axes_cor_array.set_title(f"Momentum: {momentum}MeV/c, Angle: {angle}deg \nN Reflected={reflected}", fontsize=11)
    
    return hist

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_angles_scatter_plot_mean(fig_mean, ax_mean, particle, surface_name):
    # Customize the scatter plot appearance for all momenta
    ax_mean.set_xlabel("Incident Angle (deg)", fontsize=10, fontweight='bold')
    ax_mean.set_ylabel("Reflected Angle Mean (deg)", fontsize=10, fontweight='bold')
    ax_mean.set_title(f"Angle Study - Particle: {particle}, Surface: {surface_name}", fontweight='bold', fontsize=12)
    ax_mean.grid(True, linestyle='--', linewidth=0.5)
    ax_mean.tick_params(axis='both', which='major', labelsize=10)
    ax_mean.spines['top'].set_visible(False)
    ax_mean.spines['right'].set_visible(False)
    ax_mean.set_ylim([0, 90])
    ax_mean.set_xlim([0, 90])
    
    # Shrink current axis by 20%
    box = ax_mean.get_position()
    ax_mean.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax_mean.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
    
    #ax_mean.set_yscale("log")
    fig_mean.savefig(f"plots/scatter_plot_mean_{particle}_{surface_name}.png")
    plt.close(fig_mean)  # Close the scatter plot figure after saving
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_angles_scatter_plot_mode(fig_mode, ax_mode, particle, surface_name):
    # Customize the scatter plot appearance for all momenta
    ax_mode.set_xlabel("Incident Angle (deg)", fontsize=10, fontweight='bold')
    ax_mode.set_ylabel("Reflected Angle Mode (deg)", fontsize=10, fontweight='bold')
    ax_mode.set_title(f"Angle Study - Particle: {particle}, Surface: {surface_name}", fontweight='bold', fontsize=12)
    ax_mode.grid(True, linestyle='--', linewidth=0.5)
    ax_mode.tick_params(axis='both', which='major', labelsize=10)
    ax_mode.spines['top'].set_visible(False)
    ax_mode.spines['right'].set_visible(False)
    ax_mode.set_ylim([0, 90])
    ax_mode.set_xlim([0, 90])
    
    # Shrink current axis by 20%
    box = ax_mode.get_position()
    ax_mode.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax_mode.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
    
    #ax.set_yscale("log")
    fig_mode.savefig(f"plots/scatter_plot_mode_{particle}_{surface_name}.png")
    plt.close(fig_mode)  # Close the scatter plot figure after saving

#=====================================================




# Main Code
#=====================================================
# Perform Analysis and Make Plots
for particle in PARTICLES:
    for surface in SURFACES:
        # Create the figure and axis objects for the scatter plot
        if ANGLES_SCATTER_PLOT:
            fig_mean, ax_mean = plt.subplots()
            fig_mode, ax_mode = plt.subplots()
            
            
        if ANGLE_HISTOGRAM_ARRAY:
            fig_angle_array, axes_angle_array = plt.subplots(len(MOMENTA), len(ANGLES), figsize=(16,16), sharex=True, sharey=True)
        if MOMENTUM_HISTOGRAM_ARRAY:
            fig_momentum_array, axes_momentum_array = plt.subplots(len(MOMENTA), len(ANGLES), figsize=(16,16), sharex=False, sharey=False)
        if CORRELATION_HISTOGRAM_ANGLE_MOMENTUM_ARRAY:
            fig_cor_array, axes_cor_array = plt.subplots(len(MOMENTA), len(ANGLES), figsize=(16,16), sharex=False, sharey=False)
        
        surface_name = return_surface_name(surface)
        

        for momentum_index, momentum in enumerate(MOMENTA):
            print("Analyzing momentum: " + str(momentum))
            
            theta_means = []
            theta_modes = []
            theta_std_devs = []
            theta_mean_errors = []
            theta_mode_errors = []
            
            momentum_means = []
            momentum_modes = []
            momentum_std_devs = []
            momentum_mean_errors = []
            momentum_mode_errors = []
            
            incident_angles = []

            for angle_index, angle in enumerate(ANGLES):
                print("Analyzing angle: " + str(angle))
                
                thetas = []  # Array of all outgoing angles
                momenta = [] # Array of all outgoing momenta
                
                path = DATA+str(surface)+'/'+particle+'/'+str(angle)+'/'+str(momentum)+'/'
                print(path)

                for file_path in os.listdir(path):
                    if not file_path.endswith(".root"): continue
                    with uproot.open(path + file_path) as file:
                        theta = file["PrimaryEvents"]["fTheta"]
                        theta = np.asarray(theta)
                        theta = theta[theta <= 90]  # Cut out transmitted events
                        thetas = np.append(thetas, theta)  # Add outgoing angles from the current file to array
                        
                        p_x = np.asarray(file["PrimaryEvents"]["fP_x"])
                        p_y = np.asarray(file["PrimaryEvents"]["fP_y"])
                        p_z = np.asarray(file["PrimaryEvents"]["fP_z"])
                        p_x = p_x[p_y >= 0]
                        p_z = p_z[p_y >= 0]
                        p_y = p_y[p_y >= 0]
                        p = np.sqrt(np.add(np.add(np.square(p_x),np.square(p_y)),np.square(p_z)))
                        momenta = np.append(momenta, p)
                
                if (len(thetas) < 10): continue
                #print(len(thetas))
                
                incident_angles.append(angle)
                
                theta_hist, theta_bin_edges = np.histogram(thetas, range=(0,90), bins='scott')
                theta_max_frequency = np.max(theta_hist)
                theta_mode_bins = np.where(theta_hist == theta_max_frequency)[0]
                theta_mode_interval = (theta_bin_edges[theta_mode_bins[0]], theta_bin_edges[theta_mode_bins[-1] + 1])
                theta_mode_error = (theta_mode_interval[1]-theta_mode_interval[0])/(2*np.sqrt(3)) # Error on histogram bin containing mode (i.e. max histogram bin); rectangular pdf
                theta_mode = np.nanmean(theta_mode_interval)
                theta_mean = np.nanmean(thetas)
                theta_std_dev = np.nanstd(thetas)
                theta_mean_error = theta_std_dev/np.sqrt(len(thetas)) # Error on mean = sigma/sqrt(n) where n is sample size

                theta_modes.append(theta_mode)
                theta_means.append(theta_mean)
                theta_std_devs.append(theta_std_dev)
                theta_mean_errors.append(theta_mean_error)
                theta_mode_errors.append(np.sqrt((theta_mode_error**2)+(theta_mean_error**2))) # Add error on hist bin and SEM (standard error on mean) in quadrature
                
                momentum_hist, momentum_bin_edges = np.histogram(momenta, range=(0,momentum), bins='scott')
                momentum_max_frequency = np.max(momentum_hist)
                momentum_mode_bins = np.where(momentum_hist == momentum_max_frequency)[0]
                momentum_mode_interval = (momentum_bin_edges[momentum_mode_bins[0]], momentum_bin_edges[momentum_mode_bins[-1] + 1])
                momentum_mode_error = (momentum_mode_interval[1]-momentum_mode_interval[0])/(2*np.sqrt(3)) # Error on histogram bin containing mode (i.e. max histogram bin); rectangular pdf
                momentum_mode = np.nanmean(momentum_mode_interval)
                momentum_mean = np.nanmean(momenta)
                momentum_std_dev = np.nanstd(momenta)
                momentum_mean_error = momentum_std_dev/np.sqrt(len(momenta)) # Error on mean = sigma/sqrt(n) where n is sample size

                momentum_modes.append(momentum_mode)
                momentum_means.append(momentum_mean)
                momentum_std_devs.append(momentum_std_dev)
                momentum_mean_errors.append(momentum_mean_error)
                momentum_mode_errors.append(np.sqrt((momentum_mode_error**2)+(momentum_mean_error**2))) # Add error on hist bin and SEM (standard error on mean) in quadrature
                
                
                if ANGLE_HISTOGRAMS:
                    # Histograms for this momentum
                    print("making angle histogram")
                    fig_h_angle, ax_h_angle = plt.subplots()
                    make_angle_histogram(fig_h_angle, ax_h_angle, thetas, theta_mode, theta_mean, theta_std_dev, particle, surface_name, momentum, angle, EVENTS, len(thetas))
                    fig_h_angle.savefig(f"plots/histogram_angle_mean_{particle}_{surface_name}_{momentum}_{angle}.png")
                    plt.close(fig_h_angle)  # Close the histogram figure after saving
                
                if MOMENTUM_HISTOGRAMS:
                    print("making momentum histogram")
                    fig_h_momentum, ax_h_momentum = plt.subplots()
                    make_momentum_histogram(fig_h_momentum, ax_h_momentum, momenta, momentum_mode, momentum_mean, momentum_std_dev, particle, surface_name, momentum, angle, EVENTS, len(thetas))
                    fig_h_momentum.savefig(f"plots/histogram_momentum_mean_{particle}_{surface_name}_{momentum}_{angle}.png")
                    plt.close(fig_h_momentum)  # Close the histogram figure after saving
                    
                if CORRELATION_HISTOGRAM_ANGLE_MOMENTUM:
                    print("making 2d histogram of angle vs momentum")
                    fig_h_cor, ax_h_cor = plt.subplots()
                    make_correlation_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, surface_name, momentum, angle, EVENTS, len(thetas))
                    fig_h_cor.savefig(f"plots/histogram_correlation_{particle}_{surface_name}_{momentum}_{angle}.png")
                    plt.close(fig_h_cor)  # Close the histogram figure after saving
                    
                if ANGLE_HISTOGRAM_ARRAY:
                    print("making angle histogram array")
                    make_angle_histogram_a(fig_angle_array, axes_angle_array[momentum_index][angle_index], thetas, theta_mode, theta_mean, theta_std_dev, particle, surface_name, momentum, angle, EVENTS, len(thetas))
                    
                if MOMENTUM_HISTOGRAM_ARRAY:
                    print("making angle histogram array")
                    make_momentum_histogram_a(fig_momentum_array, axes_momentum_array[momentum_index][angle_index], momenta, momentum_mode, momentum_mean, momentum_std_dev, particle, surface_name, momentum, angle, EVENTS, len(thetas))

                if CORRELATION_HISTOGRAM_ANGLE_MOMENTUM_ARRAY:
                    print("making angle momentum correlation histogram array")
                    hist = make_correlation_histogram_a(fig_cor_array, axes_cor_array[momentum_index][angle_index], thetas, momenta, particle, surface_name, momentum, angle, EVENTS, len(thetas))
            
            # Scatter plot with error bars for this momentum   
            if ANGLES_SCATTER_PLOT:         
                ax_mean.errorbar(incident_angles, theta_means, yerr=theta_mean_errors, fmt='o',markersize=5, markeredgecolor='black', capsize=3, elinewidth=1, markeredgewidth=0.5, ecolor='black', label=f"P = {momentum} MeV/c")
                ax_mode.errorbar(incident_angles, theta_modes, yerr=theta_mode_errors, fmt='o',markersize=5, markeredgecolor='black', capsize=3, elinewidth=1, markeredgewidth=0.5, ecolor='black', label=f"P = {momentum} MeV/c")
                
            if MOMENTUM_SCATTER_PLOT: pass


        # Customize the scatter plot appearance for all momenta
        if ANGLES_SCATTER_PLOT:
            print("making angles scatter plot of mean")
            make_angles_scatter_plot_mean(fig_mean, ax_mean, particle, surface_name)
            
            print("making angles scatter plot of mode")
            make_angles_scatter_plot_mode(fig_mode, ax_mode, particle, surface_name)
            
        if MOMENTUM_SCATTER_PLOT: pass
            
        if ANGLE_HISTOGRAM_ARRAY:
            fig_angle_array.suptitle(f"Reflected Angle Histograms - Angle versus Momentum - Particle: {particle}, Surface: {surface_name}, N Events: {EVENTS}", fontsize=14, fontweight='bold')
            fig_angle_array.tight_layout(pad=2)
            fig_angle_array.savefig(f"plots/histogram_angle_array_{particle}_{surface_name}.png")
            plt.close(fig_angle_array)  # Close the histogram figure after saving
            
        if MOMENTUM_HISTOGRAM_ARRAY:
            fig_momentum_array.suptitle(f"Reflected Momentum Histograms - Angle versus Momentum - Particle: {particle}, Surface: {surface_name}, N Events: {EVENTS}", fontsize=14, fontweight='bold')
            fig_momentum_array.tight_layout(pad=2)
            fig_momentum_array.savefig(f"plots/histogram_momentum_array_{particle}_{surface_name}.png")
            plt.close(fig_momentum_array)  # Close the histogram figure after saving
            
        if CORRELATION_HISTOGRAM_ANGLE_MOMENTUM_ARRAY:
            fig_cor_array.suptitle(f"Reflected Angle Momentum Correlation Histograms - Angle versus Momentum\nParticle: {particle}, Surface: {surface_name}, N Events: {EVENTS}", fontsize=14, fontweight='bold')
            cbar_ax = fig_cor_array.add_axes([0.93, 0.04, 0.015, 0.88])  # [left, bottom, width, height]
            cbar = fig_cor_array.colorbar(hist[3], cax=cbar_ax)
            cbar.set_label('Rate')
            fig_cor_array.tight_layout(pad=2, rect=[0,0,0.92,1])
            fig_cor_array.savefig(f"plots/histogram_correlation_array_{particle}_{surface_name}.png")
            plt.close(fig_cor_array)  # Close the histogram figure after saving