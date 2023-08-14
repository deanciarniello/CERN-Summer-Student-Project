# File: analysis.py
# Author: Dean Ciarniello
# Date: 2023-08-09

# Packages
#=====================================================
import numpy as np
from scipy.stats import *
from scipy import stats, optimize
import scipy as sc
import matplotlib.pyplot as plt
import uproot
import os
import sys
import matplotlib.colors as colors
import configparser

from analysis_helpers import *
from analysis_plotters import *

# Read configuration file
#=====================================================
if len(sys.argv) != 2:
    print("Please include a configuration file")
    sys.exit(1)
config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)


# Number of Events
#=====================================================
EVENTS=int(config['Setup']['EVENTS'])           # Will return error if this does not agree with number of events in data files
CUT=int(config['Setup']['EVENTS_CUT'])
#=====================================================


# Plotting Options
#=====================================================
# Read constants from the config file (PlotSelection section)
THETA_HISTOGRAMS = config.getboolean('PlotSelection', 'THETA_HISTOGRAMS')
PHI_HISTOGRAMS = config.getboolean('PlotSelection', 'PHI_HISTOGRAMS')
MOMENTUM_HISTOGRAMS = config.getboolean('PlotSelection', 'MOMENTUM_HISTOGRAMS')
CORRELATION_HISTOGRAM_THETA_MOMENTUM = config.getboolean('PlotSelection', 'CORRELATION_HISTOGRAM_THETA_MOMENTUM')
CORRELATION_HISTOGRAM_THETA_PHI = config.getboolean('PlotSelection', 'CORRELATION_HISTOGRAM_THETA_PHI')
THETA_HISTOGRAM_ARRAY = config.getboolean('PlotSelection', 'THETA_HISTOGRAM_ARRAY')
PHI_HISTOGRAM_ARRAY = config.getboolean('PlotSelection', 'PHI_HISTOGRAM_ARRAY')
MOMENTUM_HISTOGRAM_ARRAY = config.getboolean('PlotSelection', 'MOMENTUM_HISTOGRAM_ARRAY')
CORRELATION_HISTOGRAM_THETA_MOMENTUM_ARRAY = config.getboolean('PlotSelection', 'CORRELATION_HISTOGRAM_THETA_MOMENTUM_ARRAY')
CORRELATION_HISTOGRAM_THETA_PHI_ARRAY = config.getboolean('PlotSelection', 'CORRELATION_HISTOGRAM_THETA_PHI_ARRAY')
REFLECTED_TRANSMITTED_DECAYED_SCATTER_PLOT = config.getboolean('PlotSelection', 'REFLECTED_TRANSMITTED_DECAYED_SCATTER_PLOT')
THETAS_SCATTER_PLOT = config.getboolean('PlotSelection', 'THETAS_SCATTER_PLOT')
MOMENTUM_SCATTER_PLOT = config.getboolean('PlotSelection', 'MOMENTUM_SCATTER_PLOT')
TRANSMITTED_PARTICLES = config.getboolean('PlotSelection', 'TRANSMITTED_PARTICLES')


# Plotting Configuration
# Note: data for any permutations must be in the DATA directory
#=====================================================
# Read constants from the config file (PlottingConfiguration section)

# Read the range values for MOMENTA and ANGLES
momenta_range = list(map(int, config['PlottingParameters']['MOMENTA'].split(',')))
angles_range = list(map(float, config['PlottingParameters']['ANGLES'].split(',')))

MOMENTA = np.arange(momenta_range[0], momenta_range[1] + momenta_range[2], momenta_range[2])
ANGLES = np.arange(angles_range[0], angles_range[1] + angles_range[2], angles_range[2])
MATERIALS = list(map(int, config['PlottingParameters']['MATERIALS'].split(',')))
PARTICLES = [particle.strip() for particle in config['PlottingParameters']['PARTICLES'].split(',')]
THICKNESS = int(config['PlottingParameters']['THICKNESS'])
#=====================================================


# Data Directory
# Info: directory where the files are located
#=====================================================
DATA_DIR = config.get('Data', 'DATA_DIRECTORY')
DATA_FOLDER = config.get('Data', 'DATA_SUBDIRECTORY')
DATA = DATA_DIR+DATA_FOLDER
#=====================================================

# Extra constants for transmitted particle option
#=====================================================
refl_trans_string = "Transmitted" if TRANSMITTED_PARTICLES else "Reflected"
transmit = "_transmitted" if TRANSMITTED_PARTICLES else ""
#=====================================================


# Make appropriate directory for plots
#=====================================================
if not os.path.exists('./plots/'):
    os.mkdir('./plots/')

if not os.path.exists(f'./plots/{DATA_FOLDER}'):
    os.mkdir(f'./plots/{DATA_FOLDER}')


# Main Code
#=====================================================
# Iterate over permutations of particles, surfaces (materials), momenta, and angles of incident particles
for particle in PARTICLES:
    for material in MATERIALS:
        # Create the figure and axis objects for selected scatterplots and histogram arrays
        if THETAS_SCATTER_PLOT:
            fig_mean, ax_mean = plt.subplots()
            fig_mode, ax_mode = plt.subplots()
        
        if THETA_HISTOGRAM_ARRAY:
            fig_theta_array, axes_theta_array = plt.subplots(len(MOMENTA), len(ANGLES), figsize=(16,16), sharex=False, sharey=False)
            
        if PHI_HISTOGRAM_ARRAY:
            fig_phi_array, axes_phi_array = plt.subplots(len(MOMENTA), len(ANGLES), figsize=(16,16), sharex=False, sharey=False)
        
        if MOMENTUM_HISTOGRAM_ARRAY:
            fig_momentum_array, axes_momentum_array = plt.subplots(len(MOMENTA), len(ANGLES), figsize=(16,16), sharex=False, sharey=False)
        
        if CORRELATION_HISTOGRAM_THETA_MOMENTUM_ARRAY:
            fig_cor_array_t_m, axes_cor_array_t_m = plt.subplots(len(MOMENTA), len(ANGLES), figsize=(16,16), sharex=False, sharey=False)
            
        if CORRELATION_HISTOGRAM_THETA_PHI_ARRAY:
            fig_cor_array_t_p, axes_cor_array_t_p = plt.subplots(len(MOMENTA), len(ANGLES), figsize=(16,16), sharex=False, sharey=False)
        
        # Record surface/material name as string
        material_name = return_surface_name(material)
        

        for momentum_index, momentum in enumerate(MOMENTA):
            # Create reflected, transmitted, decayed scatterplot
            if REFLECTED_TRANSMITTED_DECAYED_SCATTER_PLOT:
                fig_rtd, ax_rtd = plt.subplots(figsize=(8,5))
            
            print("Analyzing momentum: " + str(momentum))
            
            # Initiate arrays for statistical parameters for theta
            theta_means = []
            theta_modes = []
            theta_std_devs = []
            theta_mean_errors = []
            theta_mode_errors = []
            
            # Initiate arrays for statistical parameters for phi
            phi_means = []
            phi_modes = []
            phi_std_devs = []
            phi_mean_errors = []
            phi_mode_errors = []
            
            # Initiate arrays for statistical parameters for momentum
            momentum_means = []
            momentum_modes = []
            momentum_std_devs = []
            momentum_mean_errors = []
            momentum_mode_errors = []
            
            # Record array of incident angles where there are reflected (or transmitted if TRANSMITTED_PARTICLES=True) particles
            incident_angles = []
            
            # Record number of non-decayed reflected and transmitted particles, and number of decayed particles
            n_reflected = []
            n_transmitted = []
            n_decayed = []
            n_decayed_in = []
            n_decayed_out_r = []
            n_decayed_out_t = []
            a_decay_pdgid = []
            n_absorbed = []

            for theta_index, theta_incident in enumerate(ANGLES):
                #print("Analyzing theta: " + str(theta_incident))
                
                # Initialize arrays of angles and momenta of reflected (or transmitted if TRANSMITTED_PARTICLES=True) particles for each configuration
                thetas = []
                phis = []
                momenta = []
                
                # Initialize counts
                reflected = 0
                transmitted = 0
                absorbed = 0
                decayed = 0
                decayed_in = 0
                decayed_out_r = 0
                decayed_out_t = 0
                decay_pdgid = 0
                events = 0
                
                
                # Record path to specific data files
                path1 = DATA + "output_" +str(material)+'_'+str(particle)+'_'+str(momentum)+'_'+str(theta_incident)+'.root'
                path2 = DATA + "output_" +str(material)+'_'+str(particle)+'_'+str(momentum)+'_'+str(theta_incident)+'_'+str(THICKNESS)+'.root'
                path3 = DATA + "output_" +str(material)+'_'+str(particle)+'_'+str(momentum)+'_'+str(round(theta_incident))+'.root'
                path4 = DATA + "output_" +str(material)+'_'+str(particle)+'_'+str(momentum)+'_'+str(round(theta_incident))+'_'+str(THICKNESS)+'.root'
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
                    exit()

                # Iterate through all .root files for the specified configuration
                #for file_path in os.listdir(path):
                #    if not file_path.endswith(".root"): continue
                with uproot.open(path) as file: # + file_path
                    theta_i = file["PrimaryEvents"]["fTheta"]            # Store thetas from root ntuples
                    theta_i = np.asarray(theta_i)
                    theta = theta_i[theta_i > 90] if TRANSMITTED_PARTICLES else theta_i[theta_i <= 90] # Cut out transmitted/reflected events
                    thetas = np.append(thetas, theta)                   # Add ntuple of thetas to thetas array
                    
                    phi = file["PrimaryEvents"]["fPhi"]                 # Store phis from root ntuples
                    phi = np.asarray(phi)
                    phi = phi[theta_i > 90] if TRANSMITTED_PARTICLES else phi[theta_i <= 90] # Cut out transmitted/reflected events
                    phis = np.append(phis, phi)                         # Add ntuple of phis to phis array
                    
                    p_x = np.asarray(file["PrimaryEvents"]["fP_x"])     # Store x-momentum fro root ntuples
                    p_y = np.asarray(file["PrimaryEvents"]["fP_y"])     # Store y-momentum fro root ntuples
                    p_z = np.asarray(file["PrimaryEvents"]["fP_z"])     # Store z-momentum fro root ntuples
                    p_x = p_x[p_y < 0] if TRANSMITTED_PARTICLES else p_x[p_y >= 0] # Cut out transmitted/reflected events
                    p_z = p_z[p_y < 0] if TRANSMITTED_PARTICLES else p_z[p_y >= 0]
                    p_y = p_y[p_y < 0] if TRANSMITTED_PARTICLES else p_y[p_y >= 0]
                    p = np.sqrt(np.add(np.add(np.square(p_x),np.square(p_y)),np.square(p_z)))
                    momenta = np.append(momenta, p)                     # Add ntuple of |P| to momenta array
                    
                    # Compute reflected, absorbed, transmitted, and decayed and add to current tally
                    reflected_add = len(np.asarray(file["PrimaryEvents"]["fEvent"])[np.asarray(file["PrimaryEvents"]["fTheta"]) < 90])
                    transmitted_add = len(np.asarray(file["PrimaryEvents"]["fEvent"])[np.asarray(file["PrimaryEvents"]["fTheta"]) > 90])
                    decayed_add = sum(np.logical_and(np.asarray(file["AllEvents"]["fIsDecayed"]), np.logical_not(np.asarray(file["AllEvents"]["fIsAbsorbed"]))))
                    absorbed_add = sum(np.asarray(file["AllEvents"]["fIsAbsorbed"]))
                    decayed_in_add = sum(np.asarray(file["AllEvents"]["fIsDecayedIn"]))
                    
                    decayed_out_events = np.asarray(file["AllEvents"]["fEvent"])
                    primary_events = np.asarray(file["PrimaryEvents"]["fEvent"])
                    decayed_out = np.asarray(file["AllEvents"]["fIsDecayedOut"])
                    decayed_out_event_nums = decayed_out_events[decayed_out > 0]
                    theta_decay = np.asarray(file["PrimaryEvents"]["fTheta"])[np.isin(primary_events,decayed_out_event_nums) > 0]
                    
                    decayed_out_r_add = len(theta_decay[theta_decay < 90])
                    decayed_out_t_add = len(theta_decay[theta_decay > 90])
                    
                    decay_pdgid = np.asarray(file["AllEvents"]["fDecayPDG"])
                    
                    reflected+=reflected_add
                    transmitted+=transmitted_add
                    decayed+= decayed_add
                    decayed_in+=decayed_in_add
                    decayed_out_r+=decayed_out_r_add
                    decayed_out_t+=decayed_out_t_add
                    absorbed+= absorbed_add
                    
                    events += len(np.asarray(file["AllEvents"]["fEvent"]))
                
                # Append tallys to arrays
                n_reflected.append(reflected)
                n_transmitted.append(transmitted)
                n_decayed.append(decayed)
                n_absorbed.append(absorbed)
                n_decayed_in.append(decayed_in)
                n_decayed_out_r.append(decayed_out_r)
                n_decayed_out_t.append(decayed_out_t)
                a_decay_pdgid.append(decay_pdgid)
                if events != EVENTS: print("******ERROR*****")
                if (reflected+transmitted+decayed+absorbed-decayed_out_r-decayed_out_t) != events: 
                    print("*****ERROR2*****")
                
                # Cut on configurations where there are less than CUT reflected (or transmitted if TRANSMITTED_PARTICLES=True) events (for statistical purposes)
                if (len(thetas) < CUT): continue
                #print(len(thetas))
                
                # Transform transmitted thetas
                thetas = [180-theta for theta in thetas] if TRANSMITTED_PARTICLES else thetas
                
                # Record theta_incident in as an incident theta where there are >= 5 (or transmitted if TRANSMITTED_PARTICLES=True) events
                incident_angles.append(theta_incident)
                
                # Compute the mean and std deviation from raw theta data; compute mode from histogram binning (take central value of max bin(s))
                range_th = (90,180) if TRANSMITTED_PARTICLES else (0,90)
                theta_hist, theta_bin_edges = np.histogram(thetas, range=range_th, bins='auto')
                theta_max_frequency = np.max(theta_hist)
                theta_mode, theta_mode_error = bootstrap_mode_error(np.asarray(thetas))
                theta_mean = np.nanmean(thetas)
                theta_std_dev = np.nanstd(thetas)
                theta_mean_error = theta_std_dev/np.sqrt(len(thetas))                                   # Error on mean = sigma/sqrt(n) where n is sample size

                # Append mean, mode, std dev, and errors to their respective arrays
                theta_modes.append(theta_mode)
                theta_means.append(theta_mean)
                theta_std_devs.append(theta_std_dev)
                theta_mean_errors.append(theta_mean_error)
                theta_mode_errors.append(theta_mode_error)
                
                #theta_mode_errors.append(np.sqrt((theta_mode_error**2)+(theta_mean_error**2)))          # Add error on hist bin and SEM (standard error on mean) in quadrature
                
                # Compute the mean and std deviation from raw phi data; compute mode from histogram binning (take central value of max bin(s))
                phi_hist, phi_bin_edges = np.histogram(phis, range=(0,360), bins='auto')
                phi_max_frequency = np.max(phi_hist)
                phi_mode_bins = np.where(phi_hist == phi_max_frequency)[0]
                phi_mode_interval = (phi_bin_edges[phi_mode_bins[0]], phi_bin_edges[phi_mode_bins[-1] + 1])
                phi_mode_error = (phi_mode_interval[1]-phi_mode_interval[0])/(2*np.sqrt(3))       # Error on histogram bin containing mode (i.e. max histogram bin); rectangular pdf
                phi_mode = np.nanmean(phi_mode_interval)
                phi_mean = np.nanmean(phis)
                phi_std_dev = np.nanstd(phis)
                phi_mean_error = phi_std_dev/np.sqrt(len(phis))                                   # Error on mean = sigma/sqrt(n) where n is sample size

                # Append mean, mode, std dev, and errors to their respective arrays
                phi_modes.append(phi_mode)
                phi_means.append(phi_mean)
                phi_std_devs.append(phi_std_dev)
                phi_mean_errors.append(phi_mean_error)
                phi_mode_errors.append(np.sqrt((phi_mode_error**2)+(phi_mean_error**2)))          # Add error on hist bin and SEM (standard error on mean) in quadrature
                
                # Compute the mean and std deviation from raw momentum data; compute mode from histogram binning (take central value of max bin(s))
                momentum_hist, momentum_bin_edges = np.histogram(momenta, range=(0,momentum), bins='auto')
                momentum_max_frequency = np.max(momentum_hist)
                momentum_mode_bins = np.where(momentum_hist == momentum_max_frequency)[0]
                momentum_mode_interval = (momentum_bin_edges[momentum_mode_bins[0]], momentum_bin_edges[momentum_mode_bins[-1] + 1])
                momentum_mode_error = (momentum_mode_interval[1]-momentum_mode_interval[0])/(2*np.sqrt(3)) # Error on histogram bin containing mode (i.e. max histogram bin); rectangular pdf
                momentum_mode = np.nanmean(momentum_mode_interval)
                momentum_mean = np.nanmean(momenta)
                momentum_std_dev = np.nanstd(momenta)
                momentum_mean_error = momentum_std_dev/np.sqrt(len(momenta)) # Error on mean = sigma/sqrt(n) where n is sample size

                # Append mean, mode, std dev, and errors to their respective arrays
                momentum_modes.append(momentum_mode)
                momentum_means.append(momentum_mean)
                momentum_std_devs.append(momentum_std_dev)
                momentum_mean_errors.append(momentum_mean_error)
                momentum_mode_errors.append(np.sqrt((momentum_mode_error**2)+(momentum_mean_error**2))) # Add error on hist bin and SEM (standard error on mean) in quadrature
                
                # Make individual histograms (depending on those selected at top of script)
                if THETA_HISTOGRAMS:
                    print("making theta histogram")
                    fig_h_theta, ax_h_theta = plt.subplots()
                    make_theta_histogram(fig_h_theta, ax_h_theta, thetas, theta_mode, theta_mean, theta_std_dev, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)
                    fig_h_theta.savefig(f"plots/{DATA_FOLDER}/histogram_theta_{particle}_{material_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_theta)  # Close the histogram figure after saving
                
                if PHI_HISTOGRAMS:
                    print("making phi histogram")
                    fig_h_phi, ax_h_phi = plt.subplots()
                    make_phi_histogram(fig_h_phi, ax_h_phi, phis, phi_mode, phi_mean, phi_std_dev, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)
                    fig_h_phi.savefig(f"plots/{DATA_FOLDER}/histogram_phi_{particle}_{material_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_phi)  # Close the histogram figure after saving
                
                if MOMENTUM_HISTOGRAMS:
                    print("making momentum histogram")
                    fig_h_momentum, ax_h_momentum = plt.subplots()
                    make_momentum_histogram(fig_h_momentum, ax_h_momentum, momenta, momentum_mode, momentum_mean, momentum_std_dev, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)
                    fig_h_momentum.savefig(f"plots/{DATA_FOLDER}/histogram_momentum_{particle}_{material_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_momentum)  # Close the histogram figure after saving
                    
                if CORRELATION_HISTOGRAM_THETA_MOMENTUM:
                    print("making 2d histogram of theta vs momentum")
                    fig_h_cor, ax_h_cor = plt.subplots()
                    make_correlation_theta_momentum_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)
                    fig_h_cor.savefig(f"plots/{DATA_FOLDER}/histogram_correlation_theta_momentum_{particle}_{material_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_cor)  # Close the histogram figure after saving
                    
                if CORRELATION_HISTOGRAM_THETA_PHI:
                    print("making 2d histogram of theta vs phi")
                    fig_h_cor, ax_h_cor = plt.subplots()
                    make_correlation_theta_phi_histogram(fig_h_cor, ax_h_cor, thetas, phis, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)
                    fig_h_cor.savefig(f"plots/{DATA_FOLDER}/histogram_correlation_theta_phi_{particle}_{material_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_cor)  # Close the histogram figure after saving
                    
                # Add histograms to arrays of histograms (depending on those selected at top of script)
                if THETA_HISTOGRAM_ARRAY:
                    print("making theta histogram array")
                    make_theta_histogram_a(fig_theta_array, axes_theta_array[momentum_index][theta_index], thetas, theta_mode, theta_mean, theta_std_dev, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)
                
                if PHI_HISTOGRAM_ARRAY:
                    print("making phi histogram array")
                    make_phi_histogram_a(fig_phi_array, axes_phi_array[momentum_index][theta_index], phis, phi_mode, phi_mean, phi_std_dev, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)
                
                if MOMENTUM_HISTOGRAM_ARRAY:
                    print("making momentum histogram array")
                    make_momentum_histogram_a(fig_momentum_array, axes_momentum_array[momentum_index][theta_index], momenta, momentum_mode, momentum_mean, momentum_std_dev, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)

                if CORRELATION_HISTOGRAM_THETA_MOMENTUM_ARRAY:
                    print("making theta momentum correlation histogram array")
                    hist_t_m = make_correlation_theta_momentum_histogram_a(fig_cor_array_t_m, axes_cor_array_t_m[momentum_index][theta_index], thetas, momenta, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)
                
                if CORRELATION_HISTOGRAM_THETA_PHI_ARRAY:
                    print("making theta phi correlation histogram array")
                    hist_t_p = make_correlation_theta_phi_histogram_a(fig_cor_array_t_p, axes_cor_array_t_p[momentum_index][theta_index], thetas, phis, particle, material_name, momentum, theta_incident, EVENTS, len(thetas), refl_trans_string, THICKNESS)
                  
                  
            # Scatter plot with error bars for this momentum   
            if THETAS_SCATTER_PLOT:         
                ax_mean.errorbar(incident_angles, theta_means, yerr=theta_mean_errors, fmt='o',markersize=5, markeredgecolor='black', capsize=3, elinewidth=1, markeredgewidth=0.5, ecolor='black', label=f"P = {momentum} MeV/c")
                ax_mode.errorbar(incident_angles, theta_modes, yerr=theta_mode_errors, fmt='o',markersize=5, markeredgecolor='black', capsize=3, elinewidth=1, markeredgewidth=0.5, ecolor='black', label=f"P = {momentum} MeV/c")
                
            if MOMENTUM_SCATTER_PLOT: pass
            
            # Scatterplot of N reflected, transmitted, absorbed
            if REFLECTED_TRANSMITTED_DECAYED_SCATTER_PLOT:
                make_rtd_scatter_plot(fig_rtd, ax_rtd, ANGLES, n_reflected, n_transmitted, n_decayed, n_decayed_in, n_decayed_out_r, n_decayed_out_t, n_absorbed, particle, material_name, momentum, EVENTS, THICKNESS, angles_range)
                fig_rtd.savefig(f'plots/{DATA_FOLDER}/scatter_plot_rtd_{particle}_{material_name}_{momentum}.png')
                plt.close(fig_rtd)


        # Make Scatter Plots (depending on selection at top of script)
        if THETAS_SCATTER_PLOT:
            print("making thetas scatter plot of mean")
            make_thetas_scatter_plot_mean(fig_mean, ax_mean, particle, material_name, refl_trans_string, THICKNESS, angles_range)
            fig_mean.savefig(f"plots/{DATA_FOLDER}/scatter_plot_theta_mean_{particle}_{material_name}.png")
            plt.close(fig_mode)
            
            print("making thetas scatter plot of mode")
            make_thetas_scatter_plot_mode(fig_mode, ax_mode, particle, material_name, refl_trans_string, THICKNESS, angles_range)
            fig_mode.savefig(f"plots/{DATA_FOLDER}/scatter_plot_theta_mode_{particle}_{material_name}.png")
            plt.close(fig_mode)
            
        if MOMENTUM_SCATTER_PLOT: pass
        
        # Make Histogram Arrays (depending on selection at top of script)
        if THETA_HISTOGRAM_ARRAY:
            fig_theta_array.suptitle(f"{refl_trans_string} Theta Histograms - Theta versus Momentum - Particle: {particle}, Material: {material_name}\nN Events: {EVENTS}, Thickness: {THICKNESS}mm", fontsize=14, fontweight='bold')
            fig_theta_array.tight_layout(pad=2)
            fig_theta_array.savefig(f"plots/{DATA_FOLDER}/histogram_theta_array_{particle}_{material_name}{transmit}.png")
            plt.close(fig_theta_array)  # Close the histogram figure after saving
        
        if PHI_HISTOGRAM_ARRAY:
            fig_phi_array.suptitle(f"{refl_trans_string} Phi Histograms - Theta versus Momentum - Particle: {particle}, Material: {material_name}\nN Events: {EVENTS}, Thickness: {THICKNESS}mm", fontsize=14, fontweight='bold')
            fig_phi_array.tight_layout(pad=2)
            fig_phi_array.savefig(f"plots/{DATA_FOLDER}/histogram_phi_array_{particle}_{material_name}{transmit}.png")
            plt.close(fig_phi_array)  # Close the histogram figure after saving
            
        if MOMENTUM_HISTOGRAM_ARRAY:
            fig_momentum_array.suptitle(f"{refl_trans_string} Momentum Histograms - Theta versus Momentum - Particle: {particle}, Material: {material_name}\nN Events: {EVENTS}, Thickness: {THICKNESS}mm", fontsize=14, fontweight='bold')
            fig_momentum_array.tight_layout(pad=2)
            fig_momentum_array.savefig(f"plots/{DATA_FOLDER}/histogram_momentum_array_{particle}_{material_name}{transmit}.png")
            plt.close(fig_momentum_array)  # Close the histogram figure after saving
            
        if CORRELATION_HISTOGRAM_THETA_MOMENTUM_ARRAY:
            fig_cor_array_t_m.suptitle(f"{refl_trans_string} Theta Momentum Correlation Histograms - Theta versus Momentum - Particle: {particle}, Material: {material_name}\nN Events: {EVENTS}, Thickness: {THICKNESS}mm", fontsize=14, fontweight='bold')
            cbar_ax = fig_cor_array_t_m.add_axes([0.93, 0.04, 0.015, 0.88])  # [left, bottom, width, height]
            cbar = fig_cor_array_t_m.colorbar(hist_t_m[3], cax=cbar_ax)
            cbar.set_label('Rate')
            fig_cor_array_t_m.tight_layout(pad=2, rect=[0,0,0.92,1])
            fig_cor_array_t_m.savefig(f"plots/{DATA_FOLDER}/histogram_correlation_array_theta_momentum_{particle}_{material_name}{transmit}.png")
            plt.close(fig_cor_array_t_m)  # Close the histogram figure after saving
            
        if CORRELATION_HISTOGRAM_THETA_PHI_ARRAY:
            fig_cor_array_t_p.suptitle(f"{refl_trans_string} Theta Phi Correlation Histograms - Theta versus Momentum - Particle: {particle}, Material: {material_name}, N Events: {EVENTS}, Thickness: {THICKNESS}mm", fontsize=14, fontweight='bold')
            cbar_ax = fig_cor_array_t_p.add_axes([0.93, 0.04, 0.015, 0.88])  # [left, bottom, width, height]
            cbar = fig_cor_array_t_p.colorbar(hist_t_p[3], cax=cbar_ax)
            cbar.set_label('Rate')
            fig_cor_array_t_p.tight_layout(pad=2, rect=[0,0,0.92,1])
            fig_cor_array_t_p.savefig(f"plots/{DATA_FOLDER}/histogram_correlation_array_theta_phi_{particle}_{material_name}{transmit}.png")
            plt.close(fig_cor_array_t_p)  # Close the histogram figure after saving