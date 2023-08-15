# File: analysis_helpers.py
# Author: Dean Ciarniello
# Date: 2023-08-14

# Packages
#=====================================================
import numpy as np


# Helper Functions
#=====================================================
def return_surface_name(material):
    '''
        Parameters:
            material (int):                  0 (Copper); 1 (Glass); 2 (Gold-Plated Copper); 3 (Gold)
        
        Returns:
            material_name (string):          name of corresponding surface/material
    '''
    material_name = ""
    if material == 0:
        material_name = "Copper"
    if material == 1:
        material_name = "Glass"
    if material == 2:
        material_name = "Gold-Plated-Copper"
    if material == 3:
        material_name = "Gold"
    return material_name

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

def bootstrap_mode_error(data):
    """
    Calculate the mode of a histogram along with its uncertainty using bootstrap resampling.

    Parameters:
        data (array-like): The input data for which to compute the mode.

    Returns:
        mode (float): The estimated mode of the data.
        mode_error (float): The uncertainty in the estimated mode.
    """
    # Calculate the mode for each bootstrap sample
    bootstrap_modes = []
    for _ in range(100):
        bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
        bin_counts, bin_edges = np.histogram(bootstrap_sample, bins='auto')
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bootstrap_mode = bin_centers[np.argmax(bin_counts)]
        bootstrap_modes.append(bootstrap_mode)

    # Compute the mode and its uncertainty
    mode = np.mean(bootstrap_modes)
    mode_error = np.std(bootstrap_modes)

    return mode, mode_error