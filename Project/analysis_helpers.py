# File: analysis_helpers.py
# Author: Dean Ciarniello
# Date: 2023-08-14

# Packages
#=====================================================
import numpy as np
import math


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
    if material == 4:
        material_name = "Aluminium"
    if material == 5:
        material_name = "Iron"
    if material == 6:
        material_name = "Silver"
    if material == 7:
        material_name = "Tungsten"
    if material == 8:
        material_name = "Bronze"
    if material == 9:
        material_name = "Brass"
    if material == 10:
        material_name = "Stainless-Steel"
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
        mode (float):           The estimated mode of the data.
        mode_error (float):     The uncertainty in the estimated mode.
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

# - - - - - - - - - - - - - - - - - - - - - - - - - -


def mode_helper(data):
    '''
    Estimates the mode of a distribution using auto binning. 
    Computes left and right HWHM estimates, for error on the mode.
    
    Parameters:
        data (array-like):      The input data set for which to compute the mode.
        
        
    Returns:
        mode (float):           Mode estimate of the data set
        left_hwhm (float):      The left HWHM estimate of the data set
        right_hwhm (float):     The right HWHM estimate of the data set
    '''
    
    # Estimate mode
    hist, bin_edges = np.histogram(data, bins='auto')
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    max_bin_index = np.argmax(hist)
    mode = bin_centers[max_bin_index]
    
    # Estimate HWHM values
    # Calculate the half-maximum count.
    half_max_count = max(hist) / 2

    # Calculate the indices for the bins at half-maximum.
    left_indexes = np.where(hist[:max_bin_index] <= half_max_count)[0]
    left_index = left_indexes[-1] if (len(left_indexes) > 0) else None
    right_indexes = max_bin_index + np.where(hist[max_bin_index:] <= half_max_count)[0]
    right_index = right_indexes[0] if (len(right_indexes) > 0) else None
    
    # Calculate the bin centers at half-maximum.
    left_hwhm = 0 if (left_index == None) else (bin_edges[left_index] + bin_edges[left_index + 1]) / 2.0
    right_hwhm = 90 if (right_index == None) else (bin_edges[right_index] + bin_edges[right_index + 1]) / 2.0
    
    return mode, mode - left_hwhm, right_hwhm - mode


def root_mean_squared_error(data, mean):
    '''
    Computes the Root Mean Squared Error of a data set.
    
    Parameters:
        data (array-like):  Data set for which to compute RMSE
        mean (float):       Mean of data set
        
    Returns:
        rmse (float):       RMSE of the data set
    '''

    n = len(data)
    data = np.asarray(data)
    data_minus_mean = data - mean
    rmse = math.sqrt(np.sum(np.square(data_minus_mean))/n)
    
    return rmse


def shifted_mode_rmse(data, rmse, mean):
    '''
    Computes the error on the mode as sigma_m^2 = sigma_(mu)^2 + (mode - mean)^2
    
    Parameters:
        data (array):       data set
        rmse (float):       root_mean_squared_error of data
        mean (float):       mean of the data
        
    Returns:
        mode (float):       estimated mode of data set
        mode_rmse (float):  shifted rms error for an error on the mode
    '''
    
    # Estimate mode
    hist, bin_edges = np.histogram(data, bins='auto')
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    max_bin_index = np.argmax(hist)
    mode = bin_centers[max_bin_index]
    
    # Compute shifted rmse
    mode_rmse = math.sqrt(math.pow(rmse,2) + math.pow((mode - mean),2))
    
    return mode, mode_rmse

def compute_alphas(incident_momentum, reflected_momenta, incident_theta):
    '''
    Computes alpha = sqrt(p_r^2 - p_i^2*sin^2(theta))/(p_i*cos(theta))
    
    Parameters:
        incident_momenta (float)
        reflected_momenta (float array)
        incident_theta[degrees] (float)
        
    Returns:
        alpha (float)
    '''
    theta_inc_rad = math.radians(incident_theta)
    p_i_term1 = (incident_momentum*math.sin(theta_inc_rad))**2
    p_i_term2 = incident_momentum*math.cos(theta_inc_rad)
    
    # compute array of alphas
    print(p_i_term1)
    print(reflected_momenta[0]**2)
    alphas = []
    for mom in reflected_momenta:
        alpha = np.sqrt(np.square(mom) - p_i_term1)/p_i_term2
        alphas.append(alpha)
    
    return alphas