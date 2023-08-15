# File: analysis_plotters.py
# Author: Dean Ciarniello
# Date: 2023-08-14

# Packages
#=====================================================
import numpy as np
from scipy.stats import *
from scipy import stats, optimize
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from analysis_helpers import *


# Functions to setup and make plots for analysis.py
#=====================================================
def setup_theta_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles

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
    n, bins, _ = ax_h.hist(thetas, bins='auto', range=range_theta, density=True, histtype='step', color='blue', linewidth=1, label=f"$\sigma: {std_dev_:.2f}$")
    
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

def make_theta_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmited particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmited particles (i.e. std dev of raw data)
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
        
        Info:
            Runs setup function to make histogram, adds title for individual histogram and adjusts height of max bin

    '''
    setup = setup_theta_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness)
    ax_h.set_title(f"Particle: {particle}, Material: {material_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}, Thickness: {thickness:.2f}mm", fontsize=11)
    ax_h.set_ylim([0,1.01*np.max(setup[0])])

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_theta_histogram_a(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            thetas (float array):           thetas of reflected/transmitted particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
        
        Info:
            Runs setup function to make histogram and adds title for array of histograms

    '''
    setup = setup_theta_histogram(fig_h, ax_h, thetas, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string)
    ax_h.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg\nN {refl_trans_string}: {refl_trans}, Thickness: {thickness:.2f}mm", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_phi_histogram(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            phis (float array):             phis of reflected/transmited particles
            mode_ (float):                  mode of phi (center of maximum histogram bin)
            mean_ (float):                  mean of phis of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of phis of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles

        Returns:
            setup (array):                  [the values of the histogram bins]
        
        Info:
            Makes a histogram of the output phi distribution of one configuration of the scattering simulation
    '''
    # Plot histogram
    n, bins, _ = ax_h.hist(phis, bins='auto', range=(0,360), density=True, histtype='step', color='blue', linewidth=1, label=f"$\sigma: {std_dev_:.2f}$")
    
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

def make_phi_histogram(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            phis (float array):             phis of reflected/transmited particles
            mode_ (float):                  mode of phis (center of maximum histogram bin)
            mean_ (float):                  mean of phis of reflected/transmited particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of phis of reflected/transmited particles (i.e. std dev of raw data)
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
        
        Info:
            Runs setup function to make histogram, adds title for individual histogram and adjusts height of max bin

    '''
    setup = setup_phi_histogram(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_title(f"Particle: {particle}, Material: {material_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}, Thickness: {thickness:.2f}mm", fontsize=11)
    ax_h.set_ylim([0,1.01*np.max(setup[0])])

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_phi_histogram_a(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            phis (float array):             phis of reflected/transmited particles
            mode_ (float):                  mode of phis (center of maximum histogram bin)
            mean_ (float):                  mean of phis of reflected/transmited particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of phis of reflected/transmited particles (i.e. std dev of raw data)
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
        
        Info:
            Runs setup function to make histogram and adds title for array of histograms

    '''
    setup = setup_phi_histogram(fig_h, ax_h, phis, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg\nN {refl_trans_string}: {refl_trans}, Thickness: {thickness:.2f}mm", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            momenta (float array):          momentum of reflected/transmitted particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         theta incident of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles

        Returns:
            setup (array):                  [the values of the histogram bins]
        
        Info:
            Makes a histogram of the output momentum distribution of one configuration of the scattering simulation
    '''
    # Plot histogram
    n, bins, _ = ax_h.hist(momenta, bins='auto', range=(0, momentum), density=True, histtype='step', color='blue', linewidth=1, label=f"$\sigma$: {std_dev_:.2f} MeV/c")
    
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

def make_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            momenta (float array):          momentum of reflected/transmited particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmited particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmited particles (i.e. std dev of raw data)
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
        
        Info:
            Runs setup function to make histogram, adds title for individual histogram and adjusts height of max bin
    '''
    setup = setup_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_ylim([0,1.01*np.max(setup[0])])
    ax_h.set_title(f"Particle: {particle}, Material: {material_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}, Thickness: {thickness:.2f}mm", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_momentum_histogram_a(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_h (matplotlib figure):      figure of plot
            ax_h (matplotlib axes):         axes of plot
            momenta (float array):          momentum of reflected/transmitted particles
            mode_ (float):                  mode of theta (center of maximum histogram bin)
            mean_ (float):                  mean of thetas of reflected/transmitted particles (i.e. mean of raw data)
            std_dev_ (float):               standard deviation of thetas of reflected/transmitted particles (i.e. std dev of raw data)
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmitted particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
        
        Info:
            Runs setup function to make histogram and adds title for array of histograms
    '''
    setup = setup_momentum_histogram(fig_h, ax_h, momenta, mode_, mean_, std_dev_, particle, material_name, momentum, theta_incident, total, refl_trans)
    ax_h.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nN {refl_trans_string}={refl_trans}, Thickness: {thickness:.2f}mm", fontsize=11)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_correlation_theta_momentum_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string):
    '''
        Parameters:
            fig_h_cor (matplotlib figure):  figure of plot
            ax_h_cor (matplotlib axes):     axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            momenta (float array):          momentum of reflected/transmited particles
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles

        Returns:
            setup (matplotlib histogram):   2d matplotlib histogram
            
        Info:
            Makes a 2d histogram of the output momentum distribution vs the output theta distribution of one configuration of the scattering simulation
    '''
    
    # Compute Correlation (Pearson)
    correlation = np.corrcoef(thetas, momenta)
    
    # Setup Histogram
    range_theta = (0,90)
    counts_theta, bins_theta = np.histogram(thetas, bins='auto', range=range_theta, density = False)
    counts_momentum, bins_momentum = np.histogram(momenta, bins='auto', range=(0,momentum), density = False)
    hist = ax_h_cor.hist2d(thetas, momenta, bins=[bins_theta, bins_momentum], cmap='Greys',density = True, norm=colors.LogNorm())
    ax_h_cor.set_ylabel(f"{refl_trans_string} Momentum (MeV/c)", fontsize=10)
    ax_h_cor.set_xlabel(f"{refl_trans_string} Theta (deg)", fontsize=10)
    
    setup = [hist, correlation[0][1]]
    return setup
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_theta_momentum_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_h_cor (matplotlib figure):  figure of plot
            ax_h_cor (matplotlib axes):     axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            momenta (float array):          momentum of reflected/transmited particles
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
            
        Info:
            Runs setup function for 2d histogram, adds title for individual 2d histogram and adds a colorbar + label
    '''
    setup = setup_correlation_theta_momentum_histogram(fig_h_cor, ax_h_cor, thetas, momenta, particle, material_name, momentum, theta_incident, total, refl_trans)
    ax_h_cor.set_title(f"Particle: {particle}, Material: {material_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}, Thickness: {thickness:.2f}mm, Corr: {setup[1]:.2f}", fontsize=11)
    
    # Add color bar for the intensity scale
    cbar = fig_h_cor.colorbar(setup[0][3], ax=ax_h_cor)
    cbar.set_label('Rate')

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_theta_momentum_histogram_a(fig_cor_array, axes_cor_array, thetas, momenta, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_cor_array (matplotlib figure):  figure of plot
            axes_cor_array (matplotlib axes):   axes of plot
            thetas (float array):               thetas of reflected/transmited particles
            momenta (float array):              momentum of reflected/transmited particles
            particle (string):                  name of particle
            material_name (string):              name of scattering surface/material
            momentum (float):                   momentum of incident particle
            theta_incident (float):             incident theta of particle
            total (int):                        total number of particles for configuration
            refl_trans (int):                   number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
            setup[0] (2d histogram):           2d histogram (for purposes of aligning the array colorbar with all the histograms in the array)
        Info:
            Runs setup function for 2d histogram and adds title for array of 2d histogram
    '''
    setup = setup_correlation_theta_momentum_histogram(fig_cor_array, axes_cor_array, thetas, momenta, particle, material_name, momentum, theta_incident, total, refl_trans)
    axes_cor_array.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nN {refl_trans_string}={refl_trans}, Thickness: {thickness:.2f}mm, Corr: {setup[1]:.2f}", fontsize=11)
    
    return setup[0]
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_correlation_theta_phi_histogram(fig_h_cor, ax_h_cor, thetas, phis, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string):
    '''
        Parameters:
            fig_h_cor (matplotlib figure):  figure of plot
            ax_h_cor (matplotlib axes):     axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            phis (float array):             phi of reflected/transmited particles
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles

        Returns:
            setup (matplotlib histogram):   2d matplotlib histogram
            
        Info:
            Makes a 2d histogram of the output phi distribution vs the output theta distribution of one configuration of the scattering simulation
    '''
    
    # Compute Correlation (Pearson)
    correlation = np.corrcoef(thetas, phis)
    
    # Setup Histogram
    range_theta = (0,90)
    range_phi = (0,360)
    counts_theta, bins_theta = np.histogram(thetas, bins='auto', range=range_theta, density = False)
    counts_phi, bins_phi = np.histogram(phis, bins='auto', range=range_phi, density = False)
    hist = ax_h_cor.hist2d(thetas, phis, bins=[bins_theta, bins_phi], cmap='Greys',density = True, norm=colors.LogNorm())
    ax_h_cor.set_ylabel(f"{refl_trans_string} Phi (deg)", fontsize=10)
    ax_h_cor.set_xlabel(f"{refl_trans_string} Theta (deg)", fontsize=10)
    
    setup = [hist, correlation[0][1]]
    return setup
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_theta_phi_histogram(fig_h_cor, ax_h_cor, thetas, phis, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_h_cor (matplotlib figure):  figure of plot
            ax_h_cor (matplotlib axes):     axes of plot
            thetas (float array):           thetas of reflected/transmited particles
            phis (float array):             phi of reflected/transmited particles
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            momentum (float):               momentum of incident particle
            theta_incident (float):         incident theta of particle
            total (int):                    total number of particles for configuration
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans (int):               number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
            
        Info:
            Runs setup function for 2d histogram, adds title for individual 2d histogram and adds a colorbar + label
    '''
    setup = setup_correlation_theta_phi_histogram(fig_h_cor, ax_h_cor, thetas, phis, particle, material_name, momentum, theta_incident, total, refl_trans)
    ax_h_cor.set_title(f"Particle: {particle}, Material: {material_name}, Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nEvents: Total={total}, {refl_trans_string}={refl_trans}, Thickness: {thickness:.2f}mm, Corr: {setup[1]:.2f}", fontsize=11)
    
    # Add color bar for the intensity scale
    cbar = fig_h_cor.colorbar(setup[0][3], ax=ax_h_cor)
    cbar.set_label('Rate')

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_correlation_theta_phi_histogram_a(fig_cor_array, ax_cor_array, thetas, phis, particle, material_name, momentum, theta_incident, total, refl_trans, refl_trans_string, thickness):
    '''
        Parameters:
            fig_cor_array (matplotlib figure):  figure of plot
            axes_cor_array (matplotlib axes):   axes of plot
            thetas (float array):               thetas of reflected/transmited particles
            phis (float array):                 phi of reflected/transmited particles
            particle (string):                  name of particle
            material_name (string):              name of scattering surface/material
            momentum (float):                   momentum of incident particle
            theta_incident (float):             incident theta of particle
            total (int):                        total number of particles for configuration
            refl_trans (int):                   number of reflected/transmited particles for configuration (excluding decayed particles)
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)

        Returns:
            setup[0] (2d histogram):           2d histogram (for purposes of aligning the array colorbar with all the histograms in the array)
        Info:
            Runs setup function for 2d histogram and adds title for array of 2d histogram
    '''
    setup = setup_correlation_theta_phi_histogram(fig_cor_array, ax_cor_array, thetas, phis, particle, material_name, momentum, theta_incident, total, refl_trans)
    ax_cor_array.set_title(f"Momentum: {momentum}MeV/c, Theta: {theta_incident}deg \nN {refl_trans_string}={refl_trans}, Thickness: {thickness:.2f}mm, Corr: {setup[1]:.2f}", fontsize=11)
    
    return setup[0]
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def setup_thetas_scatter_plot(fig, ax, particle, material_name, thickness, angles_range):
    '''
        Parameters:
            fig (matplotlib figure):        figure of plot
            ax (matplotlib axes):           axes of plot
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            thickness (float):              thickness of the plate (in mm)
            angles_range (float, float, float):  start, stop, step of provided angles range

        Returns:
        
        Info:
            Sets the title, grid params, axes limits, legend, and plot position for angles scatter plots
    '''
    # Set title, grid params, and axes limits
    ax.set_title(f"Theta Study - Particle: {particle}, Material: {material_name}, Thickness: {thickness:.2f}mm", fontsize=12)
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim([max(0, angles_range[0]-5), min(90, angles_range[1]+angles_range[2]+5)])
    ax.set_xlim([max(0, angles_range[0]-5), min(90, angles_range[1]+angles_range[2]+5)])
    
    # Plot identity line
    ax.plot(np.linspace(0, 90, 90), np.linspace(0, 90, 90), color='black', marker='', alpha=0.5, zorder=0)
    
    # Shrink y axis by 20% to make room for legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_thetas_scatter_plot_mean(fig_mean, ax_mean, particle, material_name, refl_trans_string, thickness, angles_range):
    '''
        Parameters:
            fig_mean (matplotlib figure):   figure of plot
            ax_mean (matplotlib axes):      axes of plot
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)
            angles_range (float, float, float):  start, stop, step of provided angles range

        Returns:
        
        Info:
            Sets the axis labels, make scatter plot of means of theta distributions, and save to plots directory
    '''
    # Set axis labels and run setup function
    ax_mean.set_xlabel("Incident Theta (deg)", fontsize=10, fontweight='bold')
    ax_mean.set_ylabel(f"{refl_trans_string} Theta Mean (deg)", fontsize=10, fontweight='bold')
    setup_thetas_scatter_plot(fig_mean, ax_mean, particle, material_name, thickness, angles_range)
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_thetas_scatter_plot_mode(fig_mode, ax_mode, particle, material_name, refl_trans_string, thickness, angles_range):
    '''
        Parameters:
            fig_mode (matplotlib figure):   figure of plot
            ax_mode (matplotlib axes):      axes of plot
            particle (string):              name of particle
            material_name (string):          name of scattering surface/material
            refl_trans_string (int):        string corresponding to whether the plots are for reflected or transmitted particles
            thickness (float):              thickness of the plate (in mm)
            angles_range (float, float, float):  start, stop, step of provided angles range

        Returns:
        
        Info:
            Sets the axis labels, make scatter plot of modes of theta distributions, and save to plots directory
    '''
    # Customize the scatter plot appearance for all momenta
    ax_mode.set_xlabel("Incident Theta (deg)", fontsize=10, fontweight='bold')
    ax_mode.set_ylabel(f"{refl_trans_string} Theta Mode (deg)", fontsize=10, fontweight='bold')
    setup_thetas_scatter_plot(fig_mode, ax_mode, particle, material_name, thickness, angles_range)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_rtd_scatter_plot(fig_rtd, ax_rtd, inc_angles, n_reflected, n_transmitted, n_decayed, n_decayed_in, n_decayed_out_r, n_decayed_out_t, n_absorbed, particle, material_name, momentum, total, thickness, angles_range):
    '''
        Parameters:
            fig_rtd (matplotlib figure):        figure of plot
            ax_rtd (matplotlib axes):           axes of plot
            inc_angles (float array):           array of incident thetas
            n_reflected (int array):            number of reflected particles
            n_transmitted (int array):          number of transmitted particles
            n_decayed (int array):              number of decayed particles
            n_absorbed (int array):             number of absorbed particles
            material_name (string):              name of surface/material
            momentum (float):                   incident particle momentum
            total (int):                        total number of events
            thickness (float):              thickness of the plate (in mm)
            angles_range (float, float, float):  start, stop, step of provided angles range

        Returns:
        
        Info:
            Produces a scatter plot for one momentum and material/surface configuration, of the number of 
            reflected, transmitted, absorbed, and decayed particles
    '''
    # Create a twin y-axis for decayed particles
    ax2 = ax_rtd.twinx()
    ax2.plot(inc_angles, n_decayed_out_r, color="tab:blue", marker='+', label='Decayed Out (R)', zorder=1)
    ax2.plot(inc_angles, n_decayed_out_t, color="tab:orange", marker='+', label='Decayed Out (T)', zorder=1)
    ax2.plot(inc_angles, n_decayed_in, color="tab:green", marker='+', label='Decayed In', zorder=2)
    ax2.set_ylabel('Count - Decayed', color='red', fontsize=9, fontweight='bold')
    ax2.tick_params(axis='both', which='major', labelsize=10)
    
    # Make Scatter Plots
    ax_rtd.plot(inc_angles, n_reflected, color="tab:blue", marker='o', label="Reflected", zorder=5)
    ax_rtd.plot(inc_angles, n_transmitted, color="tab:orange", marker='o', label="Transmitted", zorder=3)
    ax_rtd.plot(inc_angles, n_absorbed, marker='o', color="tab:green", label="Absorbed", zorder=2)
    ax_rtd.set_xlabel("Incident Angle (deg)", fontsize=9, fontweight='bold')
    ax_rtd.set_ylabel("Count", fontsize=9, fontweight='bold')
    ax_rtd.tick_params(axis='both', which='major', labelsize=10)

    # Adding legend for both datasets
    lines, labels = ax_rtd.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    #ax_rtd.legend(lines + lines2, labels + labels2, loc='center left')
    
    # Label axes and title
    ax_rtd.set_title(f"Angle Study\n Particle: {particle}, Material: {material_name}, Momentum: {momentum} MeV/c\nN Events = {total}, Thickness: {thickness:.2f}mm", fontsize=11)
    ax_rtd.grid(True, linestyle='--', linewidth=0.5)
    
    # Set up spines and axes limits
    ax_rtd.spines['top'].set_visible(False)
    ax_rtd.spines['right'].set_visible(False)
    ax_rtd.set_xlim([angles_range[0], angles_range[1]+angles_range[2]])
    ax_rtd.set_ylim([-0.05*total,1.05*total])
    ax2.set_ylim([-0.05*max(n_decayed_out_r+n_decayed_out_t),1.05*max(n_decayed_out_r+n_decayed_out_t)] if (max(n_decayed_out_r+n_decayed_out_t)>0) else [-0.05*5, 1.05*5])
    
    # Shrink y axis by 20% to make room for legend
    box1 = ax_rtd.get_position()
    box2 = ax2.get_position()
    ax_rtd.set_position([box1.x0, box1.y0, box1.width * 0.8, box1.height])
    ax2.set_position([box2.x0, box2.y0, box2.width * 0.8, box2.height])

    # Put a legend to the right of the current axis
    ax_rtd.legend(lines + lines2, labels + labels2, loc='center left', bbox_to_anchor=(1.1, 0.85), fontsize=8)

# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_cutoff_angle_scatterplot(fig_cutoff, ax_cutoff, momenta, cutoff_angles, cut, material_name, particle, total, refl_trans_string, thickness):
    '''
    '''
    ax_cutoff.plot(momenta, cutoff_angles, marker='o', markeredgecolor='black', label="Cutoff Theta")
    
    # Set title, grid params, and axes limits
    ax_cutoff.set_title(f"Cutoff Theta - Particle: {particle}, Material: {material_name}, Thickness: {thickness:.2f}mm\n Events: Total = {total}, Cut = {cut}", fontsize=12)
    ax_cutoff.grid(True, linestyle='--', linewidth=0.5)
    ax_cutoff.tick_params(axis='both', which='major', labelsize=10)
    ax_cutoff.spines['top'].set_visible(False)
    ax_cutoff.spines['right'].set_visible(False)
    ax_cutoff.set_xlim([min(momenta)-0.05*max(momenta), 1.05*max(momenta)])
    ax_cutoff.set_ylim([-0.05*90,90*1.05])
    
    ax_cutoff.legend(fontsize=8)
    
    ax_cutoff.set_xlabel("Incident Momentum (MeV/c)", fontsize=10, fontweight='bold')
    ax_cutoff.set_ylabel(f"{refl_trans_string} Cutoff Theta (deg)", fontsize=10, fontweight='bold')
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def make_2dhist_momenta_inc_angle(fig_mom_inc, ax_mom_inc, momentum_distributions, incident_angles, particle, material_name, momentum, total, thickness, refl_trans_string):
    # Create a 2D histogram grid
    # Create individual 1D histograms for each incident angle
    histograms = [np.histogram(momenta, bins=20, range=(0, momentum), density=True)[0] for momenta in momentum_distributions]

    # Combine individual histograms into a 2D histogram
    hist2d = np.array(histograms)

    # Plot the 2D histogram
    im = ax_mom_inc.imshow(
        hist2d.T, extent=[min(incident_angles), 90, 0, momentum],
        origin='lower', aspect='auto', cmap='inferno'
    )
    
    # Add color bar for the intensity scale
    cbar = fig_mom_inc.colorbar(im, ax=ax_mom_inc)
    cbar.set_label('Rate')

    ax_mom_inc.set_ylabel(f'{refl_trans_string} Momentum (MeV/c)')
    ax_mom_inc.set_xlabel('Incident Angle (deg)')
    ax_mom_inc.set_title(f'2D Histogram of Momenta vs Incident Angle\nParticle: {particle}, Momentum: {momentum}MeV/c, Material: {material_name}, Thickness: {thickness:.2f}mm', fontsize=12)






