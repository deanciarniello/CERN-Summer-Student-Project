<p align="center">
 <img width=300px height=300px src="misc/img.png" alt="Project logo"></a>
</p>

<h3 align="center">Geant4 Scattering Simulaton - CERN Summer Student Program 2023</h3>

<p align="center">
 <img width=123px height=40px src="https://geant4.org/assets/logo/g4logo-full-500x167.png" alt="Project logo"></a>
 <img width=140px height=40px src="https://root.cern/img/logos/ROOT_Logo/misc/generic-logo-color-plustext-512.png" alt="Project logo"></a>
</p>

---

<p align="center"> A comprehensive flat scattering Geant4 simulation with angle, material, particle type, particle momentum, and plate thickness as parameters. Options for visualization or batches, with ROOT ntuple outputs. Analysis scripts produce histograms (both arrays and individual) of momentum and angle of reflected particles, and scatter plots with errors of the means and modes of the reflected angle distributions (with matplotlib).
    <br> 
</p>

## Table of Contents

- [Simulation](#simulation)
    - [Visualisation](#visualization)
    - [Batch](#batch)
- [Analysis](#analysis)
- [Additional Notes](#notes)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgements](#acknowledgements)

## Simulation <a name="simulation"></a>

### Visualization <a name="visualization"></a>
Visualization allows the user to interact with the simulation and observe visually how the simulation works.

To run the simulation in visualization mode, you must first make a build directory and compile the simulation. From the project directory, run the following commands:
```bash
mkdir build
cd build
cmake3 .. #(or cmake ..)
make
```
Now that the simulation is compiled, you can run it directly with a command line argument:
```
./simulation [mac_file] [plate_material] [beam_angle] [beam_momentum] [beam_particle_type] [output_file] [output_dir] [visualization] [plate_thickness]
```
Parameters:
1. **mac_file**: The path to the mac file being used. For visualization, the prepared .mac file for visualization is mac/vis.mac.
2. **plate_material**: There are three plate materials: Copper (parameter 0), Glass (parameter 1), and Gold-Plated Copper (parameter 2)
3. **beam_angle**: The incident angle of the particles (in degrees). 0 degrees is perpendicular to the plate surface, 90 degrees is parallel with the plate surface.
4. **beam_momentum**: The incident momentum (in MeV) of the particles.
5. **beam_particle_type**: The beam particle type (e.g. mu-, mu+, e-, proton, etc).
6. **output_file**: The name of the output ROOT file (e.g. output.root).
7. **output_dir**: The path to the output file directory.
8. **visualization**: Enables (1) or disables (0) the visualization manager in the simulation. For visualization, always set to 1.
9. **plate_thickness**: *OPTIONAL* The thickness of the scattering plate (in mm). If no argument provided, the default thickness is 5 mm.

Once you have run this command line argument, a visualization will pop up. There may also be a number of tracks already visible, depending on whether or not this was specified in the mac/vis.mac file. In the visualization, you can further run the command 
```/run/beamOn N``` *in the visualization gui command line*, where ```N``` is the number of particles you want to run the simulation with. Old particle tracks will be removed, and the new ones will be displayed.


### Batch <a name="batch"></a>

Add notes about how to use the system.

## Analysis <a name="analysis"></a>


## Additional Notes <a name = "notes"></a>

Add additional notes about how to deploy this on a live system.

## Built Using <a name = "built_using"></a>
- <img width=20px height=20px src="https://geant4.org/assets/logo/g4logo-square.png" alt=""> [Geant4](https://geant4.cern.ch/) - Simulation Framework 
- <img width=20px height=20px src="https://root.cern/img/logos/ROOT_Logo/misc/generic-logo-color-shadowed-512.png" alt=""> [ROOT](https://root.cern/) - Data Framework 
- <img width=20px height=20px src="https://matplotlib.org/stable/_images/sphx_glr_logos2_001.png" alt=""> [Matplotlib](https://matplotlib.org/) - Plotting 
- <img width=20px height=20px src="https://raw.githubusercontent.com/numpy/numpy/main/branding/logo/secondary/numpylogo2.png" alt=""> [NumPy](https://numpy.org/) - Data Analysis  

## Authors <a name = "authors"></a>
- Dean Ciarniello [The University of British Columbia] [@deanciarniello](https://github.com/deanciarniello)

## Acknowledgements <a name = "acknowledgement"></a>

- CERN Summer Student Program
- Dr. Massimo Giovannozzi [CERN]
