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
import matplotlib.colors as colors


# Number of Events
#=====================================================
EVENTS=100000           # Will return error if this does not agree with number of events in data files
CUT=5
#=====================================================


# Plotting Options
#=====================================================
THETA_HISTOGRAMS = False
PHI_HISTOGRAMS = False
MOMENTUM_HISTOGRAMS = False
CORRELATION_HISTOGRAM_THETA_MOMENTUM = False
CORRELATION_HISTOGRAM_THETA_PHI = False

THETA_HISTOGRAM_ARRAY = False
PHI_HISTOGRAM_ARRAY = False
MOMENTUM_HISTOGRAM_ARRAY = False
CORRELATION_HISTOGRAM_THETA_MOMENTUM_ARRAY = False
CORRELATION_HISTOGRAM_THETA_PHI_ARRAY = False

REFLECTED_TRANSMITTED_DECAYED_SCATTER_PLOT = True

THETAS_SCATTER_PLOT = False
MOMENTUM_SCATTER_PLOT = False   # Not currently implemented

TRANSMITTED_PARTICLES = False    # Option for angle histograms to check transmitted particle angle distributions
                                # Not currently supported for scatterplots, only histograms/arrays

# Extra constants for transmitted particle option
#=====================================================
refl_trans_string = "Transmitted" if TRANSMITTED_PARTICLES else "Reflected"
transmit = "_transmitted" if TRANSMITTED_PARTICLES else ""
#=====================================================


# Plotting Configuration
# Note: data for any permutations must be in the DATA directory
#=====================================================
MOMENTA = range(10,210,10)
ANGLES =  range(5,90,10) #[0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70, 72.5, 75, 77.5, 80, 82.5, 85, 87.5] # 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70, 72.5, 75, 77.5, 80, 82.5, 85, 87.5
SURFACES = [0] # 0, 1, 2
PARTICLES = ["proton"] #"mu-", "e-", "proton", "mu+"
#=====================================================


# Data Directory
# Info: directory where the files are located
#=====================================================
DATA = "/eos/user/d/dciarnie/Data/output_1_v0./output_1_v0./"
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
            r_chi_squared (float):              reduced chi-squared = (sum[(obs-exp)/err]^2)/dof
    '''
    r_chi_squared = np.sum(((observed - expected) / errors) ** 2) / dof
    return r_chi_squared

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_theta_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)

        Returns:
            setup (array):                  [the values of the histogram bins]
        
        Info:
            Makes a histogram of the output theta distribution of one configuration of the scattering simulation
    '''
    # Fit to beta distribution and compute reduced chi-squared
    #params = stats.beta.fit(thetas, floc=0, fscale=90)
    #fitted_pdf = stats.beta.pdf(np.linspace(0, 90, 90), *params)
    #observed_counts, _ = np.histogram(thetas, bins=90, range=(0, 90))
    #expected_counts = len(thetas) * fitted_pdf
    #degrees_of_freedom = len(observed_counts) - len(params)         # dof = number of bins - number of fit parameters
    #reduced_chi2 = reduced_chi_squared(observed_counts[1:-1], expected_counts[1:-1], np.sqrt(expected_counts[1:-1]), degrees_of_freedom)
                       
    # Plot fitted beta distribution 
    #ax_h.plot(np.linspace(0, 90, 90), fitted_pdf,'r-', label=f'Fitted Beta Distribution \nParams: [{params[2]:.0f},{params[3]:.0f}], a={params[0]:.2f}, b={params[1]:.2f}\nChi2/dof: {reduced_chi2:.2f}')

    # Plot histogram
    range_theta = (0,90)
    n, bins, _ = ax_h.hist(thetas, bins='scott', range=range_theta, density=True, histtype='step', color='blue', linewidth=1, label=f"$\sigma: {std_dev_:.2f}$")
    
    # Plot mean, mode, and incident theta
    ax_h.axvline(mean_, 0, 1, color='black', linestyle='dashed', linewidth=1, label=f"Mean: {mean_:.2f}")
    ax_h.axvline(mode_, 0, 1, color='green', linestyle='dashed', linewidth=1, label=f"Mode: {mode_:.1f}")
    ax_h.axvline(theta_incident, 0, 1, color='red', linewidth=4, alpha=0.5, label=f"Incident Theta: {theta_incident:.2f}")
    
    # Set axis labels
    ax_h.set_xlabel(f"{refl_trans_string} Theta (deg)", fontsize=10)
    ax_h.set_ylabel("Normalized Rate", fontsize=10)
    ax_h.yaxis.set_label_position("left")
    
    # Grid and tick mark settings
    ax_h.grid(True, linestyle='--', linewidth=0.5)
    ax_h.tick_params(axis='both', which='major', labelsize=10)
    ax_h.spines['top'].set_visible(False)
    ax_h.spines['right'].set_visible(False)
    ax_h.yaxis.tick_left()
    
    # Make legend
    ax_h.legend(fontsize=8)

    # Return setup (array of anything needed from this function)
    setup = [n]
    return setup

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_theta_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmited particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmited particles (i.e. std dev of raw data)
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
        
        Info:
            Runs setup function to make histogram, adds title for individual histogram and adjusts height of max bin

    '''
    setup = setup_theta_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_title(f"Particle: {particle}, Surface: {surface_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}", fontsize=11)
    ax_h.set_ylim([0,1.01*np.max(setup[0])])

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_theta_histogram_a(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            thetas (float array):           thetas of reflected/transmitted particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)

        Returns:
        
        Info:
            Runs setup function to make histogram and adds title for array of histograms

    '''
    setup = setup_theta_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg\nN {refl_trans_string}: {refl_trans}", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_phi_histogram(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            phis (float array):             phis of reflected/transmited particles
            mode_ (float):                  mode of phi (center of maximum histogram bin)
            mean_ (float):                  mean of phis of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of phis of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)

        Returns:
            setup (array):                  [the values of the histogram bins]
        
        Info:
            Makes a histogram of the output phi distribution of one configuration of the scattering simulation
    '''
    # Plot histogram
    n, bins, _ = ax_h.hist(phis, bins='scott', range=(0,360), density=True, histtype='step', color='blue', linewidth=1, label=f"$\sigma: {std_dev_:.2f}$")
    
    # Plot mean, mode, and incident phi
    ax_h.axvline(mean_, 0, 1, color='black', linestyle='dashed', linewidth=1, label=f"Mean: {mean_:.2f}")
    ax_h.axvline(mode_, 0, 1, color='green', linestyle='dashed', linewidth=1, label=f"Mode: {mode_:.1f}")
    ax_h.axvline(180, 0, 1, color='red', linewidth=4, alpha=0.5, label=f"Incident Phi: 180")
    
    # Set axis labels
    ax_h.set_xlabel(f"{refl_trans_string} Phi (deg)", fontsize=10)
    ax_h.set_ylabel("Normalized Rate", fontsize=10)
    ax_h.yaxis.set_label_position("left")
    
    # Grid and tick mark settings
    ax_h.grid(True, linestyle='--', linewidth=0.5)
    ax_h.tick_params(axis='both', which='major', labelsize=10)
    ax_h.spines['top'].set_visible(False)
    ax_h.spines['right'].set_visible(False)
    ax_h.yaxis.tick_left()
    
    # Make legend
    ax_h.legend(fontsize=8)

    # Return setup (array of anything needed from this function)
    setup = [n]
    return setup

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_phi_histogram(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            phis (float array):             phis of reflected/transmited particles
            mode_ (float):                  mode of phis (center of maximum histogram bin)
            mean_ (float):                  mean of phis of reflected/transmited particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of phis of reflected/transmited particles (i.e. std dev of raw data)
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
        
        Info:
            Runs setup function to make histogram, adds title for individual histogram and adjusts height of max bin

    '''
    setup = setup_phi_histogram(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_title(f"Particle: {particle}, Surface: {surface_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}", fontsize=11)
    ax_h.set_ylim([0,1.01*np.max(setup[0])])

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_phi_histogram_a(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            phis (float array):             phis of reflected/transmited particles
            mode_ (float):                  mode of phis (center of maximum histogram bin)
            mean_ (float):                  mean of phis of reflected/transmited particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of phis of reflected/transmited particles (i.e. std dev of raw data)
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
        
        Info:
            Runs setup function to make histogram and adds title for array of histograms

    '''
    setup = setup_phi_histogram(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg\nN {refl_trans_string}: {refl_trans}", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            momenta (float array):          momentum of reflected/transmitted particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         theta incident of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)

        Returns:
            setup (array):                  [the values of the histogram bins]
        
        Info:
            Makes a histogram of the output momentum distribution of one configuration of the scattering simulation
    '''
    # Plot histogram
    n, bins, _ = ax_h.hist(momenta, bins='scott', range=(0, momentum), density=True, histtype='step', color='blue', linewidth=1, label=f"$\sigma$: {std_dev_:.2f} MeV/c")
    
    # Plot mean, mode, and incident theta
    ax_h.axvline(mean_, 0, 1, color='black', linestyle='dashed', linewidth=1, label=f"Mean: {mean_:.2f} MeV/c ({(mean_/momentum)*100:.2f}% of Incident)")
    ax_h.axvline(mode_, 0, 1, color='green', linestyle='dashed', linewidth=1, label=f"Mode: {mode_:.1f} MeV/c ({(mode_/momentum)*100:.1f}% of Incident)")
    ax_h.axvline(momentum, 0, 1, color='red', linewidth=4, alpha=0.5, label=f"Incident Momentum: {momentum:.2f} MeV/c")
    
    # Set axis labels
    ax_h.set_xlabel(f"{refl_trans_string} Momentum (MeV/c)", fontsize=10)
    ax_h.set_ylabel("Normalized Rate", fontsize=10)
    ax_h.yaxis.set_label_position("left")
    
    # Grid and tick mark settings
    ax_h.grid(True, linestyle='--', linewidth=0.5)
    ax_h.tick_params(axis='both', which='major', labelsize=10)
    ax_h.spines['top'].set_visible(False)
    ax_h.spines['right'].set_visible(False)
    ax_h.yaxis.tick_left()
    
    # Make legend
    ax_h.legend(fontsize=8)
    
    # Return setup (array of anything needed from this function)
    setup = [n]
    return setup

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            momenta (float array):          momentum of reflected/transmited particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmited particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmited particles (i.e. std dev of raw data)
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
        
        Info:
            Runs setup function to make histogram, adds title for individual histogram and adjusts height of max bin
    '''
    setup = setup_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_ylim([0,1.01*np.max(setup[0])])
    ax_h.set_title(f"Particle: {particle}, Surface: {surface_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_momentum_histogram_a(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            momenta (float array):          momentum of reflected/transmitted particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)

        Returns:
        
        Info:
            Runs setup function to make histogram and adds title for array of histograms
    '''
    setup = setup_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, surface_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nN {refl_trans_string}={refl_trans}", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_correlation_theta_momentum_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h_cor (matplotlib figure):  figure of plot
            ax_h_cor (matplotlib axes):     axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            momenta (float array):          momentum of reflected/transmited particles
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
            setup (matplotlib histogram):   2d matplotlib histogram
            
        Info:
            Makes a 2d histogram of the output momentum distribution vs the output theta distribution of one configuration of the scattering simulation
    '''
    
    # Compute Correlation (Pearson)
    correlation = np.corrcoef(thetas, momenta)
    
    # Setup Histogram
    range_theta = (0,90)
    counts_theta, bins_theta = np.histogram(thetas, bins='scott', range=range_theta, density = False)
    counts_momentum, bins_momentum = np.histogram(momenta, bins='scott', range=(0,momentum), density = False)
    hist = ax_h_cor.hist2d(thetas, momenta, bins=[bins_theta, bins_momentum], cmap='Greys',density = True, norm=colors.LogNorm())
    ax_h_cor.set_ylabel(f"{refl_trans_string} Momentum (MeV/c)", fontsize=10)
    ax_h_cor.set_xlabel(f"{refl_trans_string} Theta (deg)", fontsize=10)
    
    setup = [hist, correlation[0][1]]
    return setup
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_theta_momentum_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h_cor (matplotlib figure):  figure of plot
            ax_h_cor (matplotlib axes):     axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            momenta (float array):          momentum of reflected/transmited particles
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
            
        Info:
            Runs setup function for 2d histogram, adds title for individual 2d histogram and adds a colorbar + label
    '''
    setup = setup_correlation_theta_momentum_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, surface_name, momentum, theta_incident, total, refl_trans)
    ax_h_cor.set_title(f"Particle: {particle}, Surface: {surface_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}, Corr: {setup[1]:.2f}", fontsize=11)
    
    # Add color bar for the intensity scale
    cbar = fig_h_cor.colorbar(setup[0][3], ax=ax_h_cor)
    cbar.set_label('Rate')

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_theta_momentum_histogram_a(fig_cor_array, axes_cor_array, thetas, momenta, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_cor_array (matplotlib figure):  figure of plot
            axes_cor_array (matplotlib axes):   axes of plot
            thetas (float array):               thetas of reflected/transmited particles
            momenta (float array):              momentum of reflected/transmited particles
            particle (string):                  name of particle
            surface_name (string):              name of scattering surface/material
            momentum (float):                   momentum of incident particle
            theta_incident (float):             incident theta of particle
            total (int):                        total number of particles for configuration
            refl_trans (int):                   number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
            setup[0] (2d histogram):           2d histogram (for purposes of aligning the array colorbar with all the histograms in the array)
        Info:
            Runs setup function for 2d histogram and adds title for array of 2d histogram
    '''
    setup = setup_correlation_theta_momentum_histogram(fig_cor_array, axes_cor_array, thetas, momenta, particle, surface_name, momentum, theta_incident, total, refl_trans)
    axes_cor_array.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nN {refl_trans_string}={refl_trans}, Corr: {setup[1]:.2f}", fontsize=11)
    
    return setup[0]
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_correlation_theta_phi_histogram(fig_h_cor, ax_h_cor, thetas, phis, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h_cor (matplotlib figure):  figure of plot
            ax_h_cor (matplotlib axes):     axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            phis (float array):             phi of reflected/transmited particles
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
            setup (matplotlib histogram):   2d matplotlib histogram
            
        Info:
            Makes a 2d histogram of the output phi distribution vs the output theta distribution of one configuration of the scattering simulation
    '''
    
    # Compute Correlation (Pearson)
    correlation = np.corrcoef(thetas, momenta)
    
    # Setup Histogram
    range_theta = (0,90)
    range_phi = (0,360)
    counts_theta, bins_theta = np.histogram(thetas, bins='scott', range=range_theta, density = False)
    counts_phi, bins_phi = np.histogram(phis, bins='scott', range=range_phi, density = False)
    hist = ax_h_cor.hist2d(thetas, phis, bins=[bins_theta, bins_phi], cmap='Greys',density = True, norm=colors.LogNorm())
    ax_h_cor.set_ylabel(f"{refl_trans_string} Phi (deg)", fontsize=10)
    ax_h_cor.set_xlabel(f"{refl_trans_string} Theta (deg)", fontsize=10)
    
    setup = [hist, correlation[0][1]]
    return setup
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_theta_phi_histogram(fig_h_cor, ax_h_cor, thetas, phis, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_h_cor (matplotlib figure):  figure of plot
            ax_h_cor (matplotlib axes):     axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            phis (float array):             phi of reflected/transmited particles
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
            
        Info:
            Runs setup function for 2d histogram, adds title for individual 2d histogram and adds a colorbar + label
    '''
    setup = setup_correlation_theta_phi_histogram(fig_h_cor, ax_h_cor, thetas, phis, particle, surface_name, momentum, theta_incident, total, refl_trans)
    ax_h_cor.set_title(f"Particle: {particle}, Surface: {surface_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}, Corr: {setup[1]:.2f}", fontsize=11)
    
    # Add color bar for the intensity scale
    cbar = fig_h_cor.colorbar(setup[0][3], ax=ax_h_cor)
    cbar.set_label('Rate')

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_theta_phi_histogram_a(fig_cor_array, ax_cor_array, thetas, phis, particle, surface_name, momentum, theta_incident, total, refl_trans):
    '''
        Parameters:
            fig_cor_array (matplotlib figure):  figure of plot
            axes_cor_array (matplotlib axes):   axes of plot
            thetas (float array):               thetas of reflected/transmited particles
            phis (float array):                 phi of reflected/transmited particles
            particle (string):                  name of particle
            surface_name (string):              name of scattering surface/material
            momentum (float):                   momentum of incident particle
            theta_incident (float):             incident theta of particle
            total (int):                        total number of particles for configuration
            refl_trans (int):                   number of reflected/transmited particles for configuration (excluding decayed particles)

        Returns:
            setup[0] (2d histogram):           2d histogram (for purposes of aligning the array colorbar with all the histograms in the array)
        Info:
            Runs setup function for 2d histogram and adds title for array of 2d histogram
    '''
    setup = setup_correlation_theta_phi_histogram(fig_cor_array, ax_cor_array, thetas, phis, particle, surface_name, momentum, theta_incident, total, refl_trans)
    ax_cor_array.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nN {refl_trans_string}={refl_trans}, Corr: {setup[1]:.2f}", fontsize=11)
    
    return setup[0]
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_thetas_scatter_plot(fig, ax, particle, surface_name):
    '''
        Parameters:
            fig (matplotlib figure):        figure of plot
            ax (matplotlib axes):           axes of plot
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material

        Returns:
        
        Info:
            Sets the title, grid params, axes limits, legend, and plot position for angles scatter plots
    '''
    # Set title, grid params, and axes limits
    ax.set_title(f"Theta Study - Particle: {particle}, Surface: {surface_name}", fontweight='bold', fontsize=12)
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim([0, 90])
    ax.set_xlim([0, 90])
    
    # Shrink y axis by 20% to make room for legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_thetas_scatter_plot_mean(fig_mean, ax_mean, particle, surface_name):
    '''
        Parameters:
            fig_mean (matplotlib figure):   figure of plot
            ax_mean (matplotlib axes):      axes of plot
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material

        Returns:
        
        Info:
            Sets the axis labels, make scatter plot of means of theta distributions, and save to plots directory
    '''
    # Set axis labels and run setup function
    ax_mean.set_xlabel("Incident Theta (deg)", fontsize=10, fontweight='bold')
    ax_mean.set_ylabel(f"{refl_trans_string} Theta Mean (deg)", fontsize=10, fontweight='bold')
    setup_thetas_scatter_plot(fig_mean, ax_mean, particle, surface_name)
    
    # Save and close
    fig_mean.savefig(f"plots/scatter_plot_theta_mean_{particle}_{surface_name}.png")
    plt.close(fig_mean)
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_thetas_scatter_plot_mode(fig_mode, ax_mode, particle, surface_name):
    '''
        Parameters:
            fig_mode (matplotlib figure):   figure of plot
            ax_mode (matplotlib axes):      axes of plot
            particle (string):              name of particle
            surface_name (string):          name of scattering surface/material

        Returns:
        
        Info:
            Sets the axis labels, make scatter plot of modes of theta distributions, and save to plots directory
    '''
    # Customize the scatter plot appearance for all momenta
    ax_mode.set_xlabel("Incident Theta (deg)", fontsize=10, fontweight='bold')
    ax_mode.set_ylabel(f"{refl_trans_string} Theta Mode (deg)", fontsize=10, fontweight='bold')
    setup_thetas_scatter_plot(fig_mode, ax_mode, particle, surface_name)
    
    # Save and close
    fig_mode.savefig(f"plots/scatter_plot_theta_mode_{particle}_{surface_name}.png")
    plt.close(fig_mode)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_rtd_scatter_plot(fig_rtd, ax_rtd, inc_angles, n_reflected, n_transmitted, n_decayed, n_decayed_in, n_decayed_out, n_absorbed, particle, surface_name, momentum, total):
    '''
        Parameters:
            fig_rtd (matplotlib figure):        figure of plot
            ax_rtd (matplotlib axes):           axes of plot
            inc_angles (float array):           array of incident thetas
            n_reflected (int array):            number of reflected particles
            n_transmitted (int array):          number of transmitted particles
            n_decayed (int array):              number of decayed particles
            n_absorbed (int array):             number of absorbed particles
            surface_name (string):              name of surface/material
            momentum (float):                   incident particle momentum
            total (int):                        total number of events
        
        Returns:
        
        Info:
            Produces a scatter plot for one momentum and material/surface configuration, of the number of 
            reflected, transmitted, absorbed, and decayed particles
    '''
    # Create a twin y-axis for decayed particles
    ax2 = ax_rtd.twinx()
    ax2.scatter(inc_angles, n_decayed_in, color="tab:green", marker='+', edgecolors='none', label='Decayed In', zorder=2)
    ax2.scatter(inc_angles, n_decayed_out, color="tab:blue", marker='+', edgecolors='none', label='Decayed Out', zorder=1)
    ax2.set_ylabel('Count - Decayed', color='red', fontsize=9, fontweight='bold')
    ax2.tick_params(axis='both', which='major', labelsize=10)
    
    # Make Scatter Plots
    ax_rtd.scatter(inc_angles, n_reflected, color="tab:blue", marker='o', edgecolors='none', label="Reflected", zorder=5)
    ax_rtd.scatter(inc_angles, n_transmitted, color="tab:orange", marker='o', edgecolors='none', label="Transmitted", zorder=3)
    #ax_rtd.scatter(inc_angles, n_decayed, marker='o', edgecolors='black', label="Decayed")
    ax_rtd.scatter(inc_angles, n_absorbed, marker='o', color="tab:green", edgecolors='none', label="Absorbed", zorder=2)
    ax_rtd.set_xlabel("Incident Angle (deg)", fontsize=9, fontweight='bold')
    ax_rtd.set_ylabel("Count", fontsize=9, fontweight='bold')
    ax_rtd.tick_params(axis='both', which='major', labelsize=10)

    # Adding legend for both datasets
    lines, labels = ax_rtd.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    #ax_rtd.legend(lines + lines2, labels + labels2, loc='center left')
    
    # Label axes and title
    ax_rtd.set_title(f"Angle Study\n Particle: {particle}, Surface: {surface_name}, Momentum: {momentum} MeV/c\nN Events = {total}", fontsize=11)
    ax_rtd.grid(True, linestyle='--', linewidth=0.5)
    
    # Set up spines and axes limits
    ax_rtd.spines['top'].set_visible(False)
    ax_rtd.spines['right'].set_visible(False)
    ax_rtd.set_xlim([0, 90])
    ax_rtd.set_ylim([-0.05*total,1.05*total])
    
    # Shrink y axis by 20% to make room for legend
    box1 = ax_rtd.get_position()
    box2 = ax2.get_position()
    ax_rtd.set_position([box1.x0, box1.y0, box1.width * 0.8, box1.height])
    ax2.set_position([box2.x0, box2.y0, box2.width * 0.8, box2.height])

    # Put a legend to the right of the current axis
    ax_rtd.legend(lines + lines2, labels + labels2, loc='center left', bbox_to_anchor=(1.1, 0.85), fontsize=8)
    
    # Make legend and save/close figure.
    fig_rtd.savefig(f'plots/scatter_plot_rtd_{particle}_{surface_name}_{momentum}.png')
    plt.close(fig_rtd)

#=====================================================


# Main Code
#=====================================================
# Iterate over permutations of particles, surfaces (materials), momenta, and angles of incident particles
for particle in PARTICLES:
    for surface in SURFACES:
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
        surface_name = return_surface_name(surface)
        

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
            n_decayed_out = []
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
                decayed_out = 0
                decay_pdgid = 0
                events = 0
                
                
                # Record path to specific data files
                #path = DATA+str(surface)+'/'+particle+'/'+str(theta_incident)+'/'+str(momentum)+'/'
                
                path = DATA + "output_" +str(surface)+'_'+str(particle)+'_'+str(momentum)+'_'+str(theta_incident)+'.root'
                #print(path)

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
                    decayed_out_add = sum(np.asarray(file["AllEvents"]["fIsDecayedOut"]))
                    decay_pdgid = np.asarray(file["AllEvents"]["fDecayPDG"])
                    
                    reflected+=reflected_add
                    transmitted+=transmitted_add
                    decayed+= decayed_add
                    decayed_in+=decayed_in_add
                    decayed_out+=decayed_out_add
                    absorbed+= absorbed_add
                    
                    events += len(np.asarray(file["AllEvents"]["fEvent"]))
                
                # Append tallys to arrays
                n_reflected.append(reflected)
                n_transmitted.append(transmitted)
                n_decayed.append(decayed)
                n_absorbed.append(absorbed)
                n_decayed_in.append(decayed_in)
                n_decayed_out.append(decayed_out)
                a_decay_pdgid.append(decay_pdgid)
                if events != EVENTS: print("******ERROR*****")
                if (reflected+transmitted+decayed+absorbed) != events: 
                    print("*****ERROR2*****")
                
                # Cut on configurations where there are less than CUT reflected (or transmitted if TRANSMITTED_PARTICLES=True) events (for statistical purposes)
                if (len(thetas) < CUT): continue
                #print(len(thetas))
                
                # Transform transmitted thetas
                thetas = [180-theta for theta in thetas] if TRANSMITTED_PARTICLES else thetas
                
                # Record theta_incident in as an incident theta where there are >= 5 (or transmitted if TRANSMITTED_PARTICLES=True) events
                incident_angles.append(theta_incident)
                
                # Compute the mean and std deviation from raw theta data; compute mode from histogram binning (take central value of max bin(s))
                range = (90,180) if TRANSMITTED_PARTICLES else (0,90)
                theta_hist, theta_bin_edges = np.histogram(thetas, range=range, bins='scott')
                theta_max_frequency = np.max(theta_hist)
                theta_mode_bins = np.where(theta_hist == theta_max_frequency)[0]
                theta_mode_interval = (theta_bin_edges[theta_mode_bins[0]], theta_bin_edges[theta_mode_bins[-1] + 1])
                theta_mode_error = (theta_mode_interval[1]-theta_mode_interval[0])/(2*np.sqrt(3))       # Error on histogram bin containing mode (i.e. max histogram bin); rectangular pdf
                theta_mode = np.nanmean(theta_mode_interval)
                theta_mean = np.nanmean(thetas)
                theta_std_dev = np.nanstd(thetas)
                theta_mean_error = theta_std_dev/np.sqrt(len(thetas))                                   # Error on mean = sigma/sqrt(n) where n is sample size

                # Append mean, mode, std dev, and errors to their respective arrays
                theta_modes.append(theta_mode)
                theta_means.append(theta_mean)
                theta_std_devs.append(theta_std_dev)
                theta_mean_errors.append(theta_mean_error)
                theta_mode_errors.append(np.sqrt((theta_mode_error**2)+(theta_mean_error**2)))          # Add error on hist bin and SEM (standard error on mean) in quadrature
                
                # Compute the mean and std deviation from raw phi data; compute mode from histogram binning (take central value of max bin(s))
                phi_hist, phi_bin_edges = np.histogram(phis, range=(0,360), bins='scott')
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
                momentum_hist, momentum_bin_edges = np.histogram(momenta, range=(0,momentum), bins='scott')
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
                    make_theta_histogram(fig_h_theta, ax_h_theta, thetas, theta_mode, theta_mean, theta_std_dev, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))
                    fig_h_theta.savefig(f"plots/histogram_theta_{particle}_{surface_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_theta)  # Close the histogram figure after saving
                
                if PHI_HISTOGRAMS:
                    print("making phi histogram")
                    fig_h_phi, ax_h_phi = plt.subplots()
                    make_phi_histogram(fig_h_phi, ax_h_phi, phis, phi_mode, phi_mean, phi_std_dev, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))
                    fig_h_phi.savefig(f"plots/histogram_phi_{particle}_{surface_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_phi)  # Close the histogram figure after saving
                
                if MOMENTUM_HISTOGRAMS:
                    print("making momentum histogram")
                    fig_h_momentum, ax_h_momentum = plt.subplots()
                    make_momentum_histogram(fig_h_momentum, ax_h_momentum, momenta, momentum_mode, momentum_mean, momentum_std_dev, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))
                    fig_h_momentum.savefig(f"plots/histogram_momentum_{particle}_{surface_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_momentum)  # Close the histogram figure after saving
                    
                if CORRELATION_HISTOGRAM_THETA_MOMENTUM:
                    print("making 2d histogram of theta vs momentum")
                    fig_h_cor, ax_h_cor = plt.subplots()
                    make_correlation_theta_momentum_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))
                    fig_h_cor.savefig(f"plots/histogram_correlation_theta_momentum_{particle}_{surface_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_cor)  # Close the histogram figure after saving
                    
                if CORRELATION_HISTOGRAM_THETA_PHI:
                    print("making 2d histogram of theta vs phi")
                    fig_h_cor, ax_h_cor = plt.subplots()
                    make_correlation_theta_phi_histogram(fig_h_cor, ax_h_cor, thetas, phis, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))
                    fig_h_cor.savefig(f"plots/histogram_correlation_theta_phi_{particle}_{surface_name}_{momentum}_{theta_incident}{transmit}.png")
                    plt.close(fig_h_cor)  # Close the histogram figure after saving
                    
                # Add histograms to arrays of histograms (depending on those selected at top of script)
                if THETA_HISTOGRAM_ARRAY:
                    print("making theta histogram array")
                    make_theta_histogram_a(fig_theta_array, axes_theta_array[momentum_index][theta_index], thetas, theta_mode, theta_mean, theta_std_dev, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))
                
                if PHI_HISTOGRAM_ARRAY:
                    print("making phi histogram array")
                    make_phi_histogram_a(fig_phi_array, axes_phi_array[momentum_index][theta_index], phis, phi_mode, phi_mean, phi_std_dev, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))
                
                if MOMENTUM_HISTOGRAM_ARRAY:
                    print("making momentum histogram array")
                    make_momentum_histogram_a(fig_momentum_array, axes_momentum_array[momentum_index][theta_index], momenta, momentum_mode, momentum_mean, momentum_std_dev, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))

                if CORRELATION_HISTOGRAM_THETA_MOMENTUM_ARRAY:
                    print("making theta momentum correlation histogram array")
                    hist_t_m = make_correlation_theta_momentum_histogram_a(fig_cor_array_t_m, axes_cor_array_t_m[momentum_index][theta_index], thetas, momenta, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))
                
                if CORRELATION_HISTOGRAM_THETA_PHI_ARRAY:
                    print("making theta phi correlation histogram array")
                    hist_t_p = make_correlation_theta_phi_histogram_a(fig_cor_array_t_p, axes_cor_array_t_p[momentum_index][theta_index], thetas, phis, particle, surface_name, momentum, theta_incident, EVENTS, len(thetas))
                  
                  
            # Scatter plot with error bars for this momentum   
            if THETAS_SCATTER_PLOT:         
                ax_mean.errorbar(incident_angles, theta_means, yerr=theta_mean_errors, fmt='o',markersize=5, markeredgecolor='black', capsize=3, elinewidth=1, markeredgewidth=0.5, ecolor='black', label=f"P = {momentum} MeV/c")
                ax_mode.errorbar(incident_angles, theta_modes, yerr=theta_mode_errors, fmt='o',markersize=5, markeredgecolor='black', capsize=3, elinewidth=1, markeredgewidth=0.5, ecolor='black', label=f"P = {momentum} MeV/c")
                
            if MOMENTUM_SCATTER_PLOT: pass
            
            # Scatterplot of N reflected, transmitted, absorbed
            if REFLECTED_TRANSMITTED_DECAYED_SCATTER_PLOT:
                make_rtd_scatter_plot(fig_rtd, ax_rtd, ANGLES, n_reflected, n_transmitted, n_decayed, n_decayed_in, n_decayed_out, n_absorbed, particle, surface_name, momentum, EVENTS)


        # Make Scatter Plots (depending on selection at top of script)
        if THETAS_SCATTER_PLOT:
            print("making thetas scatter plot of mean")
            make_thetas_scatter_plot_mean(fig_mean, ax_mean, particle, surface_name)
            
            print("making thetas scatter plot of mode")
            make_thetas_scatter_plot_mode(fig_mode, ax_mode, particle, surface_name)
            
        if MOMENTUM_SCATTER_PLOT: pass
        
        # Make Histogram Arrays (depending on selection at top of script)
        if THETA_HISTOGRAM_ARRAY:
            fig_theta_array.suptitle(f"{refl_trans_string} Theta Histograms - Theta versus Momentum - Particle: {particle}, Surface: {surface_name}, N Events: {EVENTS}", fontsize=14, fontweight='bold')
            fig_theta_array.tight_layout(pad=2)
            fig_theta_array.savefig(f"plots/histogram_theta_array_{particle}_{surface_name}{transmit}.png")
            plt.close(fig_theta_array)  # Close the histogram figure after saving
        
        if PHI_HISTOGRAM_ARRAY:
            fig_phi_array.suptitle(f"{refl_trans_string} Phi Histograms - Theta versus Momentum - Particle: {particle}, Surface: {surface_name}, N Events: {EVENTS}", fontsize=14, fontweight='bold')
            fig_phi_array.tight_layout(pad=2)
            fig_phi_array.savefig(f"plots/histogram_phi_array_{particle}_{surface_name}{transmit}.png")
            plt.close(fig_phi_array)  # Close the histogram figure after saving
            
        if MOMENTUM_HISTOGRAM_ARRAY:
            fig_momentum_array.suptitle(f"{refl_trans_string} Momentum Histograms - Theta versus Momentum - Particle: {particle}, Surface: {surface_name}, N Events: {EVENTS}", fontsize=14, fontweight='bold')
            fig_momentum_array.tight_layout(pad=2)
            fig_momentum_array.savefig(f"plots/histogram_momentum_array_{particle}_{surface_name}{transmit}.png")
            plt.close(fig_momentum_array)  # Close the histogram figure after saving
            
        if CORRELATION_HISTOGRAM_THETA_MOMENTUM_ARRAY:
            fig_cor_array_t_m.suptitle(f"{refl_trans_string} Theta Momentum Correlation Histograms - Theta versus Momentum\nParticle: {particle}, Surface: {surface_name}, N Events: {EVENTS}", fontsize=14, fontweight='bold')
            cbar_ax = fig_cor_array_t_m.add_axes([0.93, 0.04, 0.015, 0.88])  # [left, bottom, width, height]
            cbar = fig_cor_array_t_m.colorbar(hist_t_m[3], cax=cbar_ax)
            cbar.set_label('Rate')
            fig_cor_array_t_m.tight_layout(pad=2, rect=[0,0,0.92,1])
            fig_cor_array_t_m.savefig(f"plots/histogram_correlation_array_theta_momentum_{particle}_{surface_name}{transmit}.png")
            plt.close(fig_cor_array_t_m)  # Close the histogram figure after saving
            
        if CORRELATION_HISTOGRAM_THETA_PHI_ARRAY:
            fig_cor_array_t_p.suptitle(f"{refl_trans_string} Theta Phi Correlation Histograms - Theta versus Momentum\nParticle: {particle}, Surface: {surface_name}, N Events: {EVENTS}", fontsize=14, fontweight='bold')
            cbar_ax = fig_cor_array_t_p.add_axes([0.93, 0.04, 0.015, 0.88])  # [left, bottom, width, height]
            cbar = fig_cor_array_t_p.colorbar(hist_t_p[3], cax=cbar_ax)
            cbar.set_label('Rate')
            fig_cor_array_t_p.tight_layout(pad=2, rect=[0,0,0.92,1])
            fig_cor_array_t_p.savefig(f"plots/histogram_correlation_array_theta_phi_{particle}_{surface_name}{transmit}.png")
            plt.close(fig_cor_array_t_p)  # Close the histogram figure after saving