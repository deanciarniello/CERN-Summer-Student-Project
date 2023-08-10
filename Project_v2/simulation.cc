/*
File: simulation.cc
Author: Dean Ciarniello
Date: 2023-08-09
*/

// Includes
// ===================================================
#include <iostream>
#include <stdio.h>
#include <sstream>

#include "G4RunManagerFactory.hh"
#include "G4UImanager.hh"
#include "G4VisManager.hh"
#include "G4UIExecutive.hh"
#include "G4VisExecutive.hh"

#include "DetectorConstruction.hh"
#include "PhysicsList.hh"
#include "Action.hh"

// Main
// ===================================================
int main(int argc, char** argv) {
    // Read in command line arguments and store in respective variables
    //
    // argv:
    // ---------------------------------
    // 1) .mac file
    // 2) capillary material
    // 3) capillary shape (0 -> Polynomial of the form p_n(x) = ax^n+b; 1 -> Hyperbola h(x) = a*sqrt(1+(x/b)^2) + c)
    // 4) capillary config (for 0 capillary shape: polyOrder,startRad,endRad,length,thickness,numZPlanes)
    //                     (for 1 capillary shape: startRad,endRad,length,thickness,numZPlanes)
    //                      *** all lengths in mm
    // 5) output file name
    // 6) path to output file
    // 7) visualization {0,1}
    // ---------------------------------
    // (Beam Setup)
    // 8) particle type
    // 9) radius of beam
    // 10) sigma of beam angle (degrees)
    // 11) beam energy (NOT MOMENTUM) in MeV
    // 12) beam energy sigma
    G4int capillaryMaterial = std::stoi(argv[2]);
    G4int capillaryShape = std::stoi(argv[3]);
    G4String outputFile = argv[5];
    G4String outputFilePath = argv[6];
    G4int vis = std::stoi(argv[7]);

    // convert capillary config to a vector
    std::vector<G4double> capillaryConfig;
    std::string str_config;
    G4double d_config;
    std::stringstream ss(argv[4]);
    while (getline(ss, str_config, ',')){
        d_config = std::stod(str_config);
        capillaryConfig.push_back(d_config);
        G4cout << d_config << G4endl;
    }

    // Create run manager, and set user initializions: detector construction, physics list, and action
    auto *runManager = G4RunManagerFactory::CreateRunManager();
    runManager->SetUserInitialization(new DetectorConstruction(capillaryMaterial, capillaryShape, capillaryConfig));
    runManager->SetUserInitialization(new PhysicsList());
    runManager->SetUserInitialization(new ActionInitialization(outputFile, outputFilePath));
    
    // Initialize run manager
    runManager->Initialize();

    // If ui enabled, define and initialize vis manager
    G4UIExecutive *ui = nullptr;
    G4VisManager *visManager = nullptr;
    if (vis) { 
        ui = new G4UIExecutive(argc, argv);
        visManager = new G4VisExecutive();
        visManager->Initialize();
    }

    // Get pointer to UI manager
    G4UImanager *UImanager = G4UImanager::GetUIpointer();

    // Set up general particle source
    if (!vis) {
        G4String particle = argv[8];
        UImanager->ApplyCommand("/gps/particle "+particle);
        UImanager->ApplyCommand("/gps/pos/type Beam");
        UImanager->ApplyCommand("/gps/pos/shape Circle");
        UImanager->ApplyCommand("/gps/pos/centre 0. 0. 0. m");
        G4String radius = argv[9];
        UImanager->ApplyCommand("/gps/pos/radius "+radius+" mm");
        UImanager->ApplyCommand("/gps/ang/type beam1d");
        G4String angle_sigma = argv[10];
        UImanager->ApplyCommand("/gps/ang/sigma_r "+angle_sigma+" deg");
        UImanager->ApplyCommand("/gps/ene/type Gauss");
        G4String beam_energy = argv[11];
        UImanager->ApplyCommand("/gps/ene/mono "+beam_energy+" MeV");
        G4String energy_sigma = argv[12];
        UImanager->ApplyCommand("/gps/ene/sigma "+energy_sigma+" MeV");
    }

    // Execute .mac file
    G4String command = "/control/execute ";
    G4String fileName = argv[1];
    UImanager->ApplyCommand(command+fileName);
    
    // If vis enabled, start the session
    if (vis) { ui->SessionStart(); }

    // Delete run, vis, and ui managers
    delete runManager;
    if (vis) {
        delete visManager;
        delete ui;
    }

    return 0;
}