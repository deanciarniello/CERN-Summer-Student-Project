/*
File: simulation.cc
Author: Dean Ciarniello
Date: 2023-07-22
*/

// Includes
// ===================================================
#include <iostream>
#include <stdio.h>

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
    // 1) .mac file
    // 2) detector config (plate material)
    // 3) beam angle (w.r.t normal)
    // 4) beam momentum (MeV/c)
    // 5) beam particle type
    // 6) output file name
    // 7) path to output file
    // 8) visualization {0,1}
    // 9) plate thickness (in mm) [OPTIONAL]

    G4int detectorConfig = std::stoi(argv[2]);
    G4double beamAngle = std::stod(argv[3]);
    G4double beamPMeV = std::stod(argv[4]);
    G4String beamParticleType = argv[5];
    G4String outputFile = argv[6];
    G4String outputFilePath = argv[7];
    G4int vis = std::stoi(argv[8]);
    G4double plateThickness;
    if (argv[9] == NULL) {
        plateThickness = 5; // default thickness is 5 mm
    } else {
        plateThickness = std::stod(argv[9]);
    }

    // Create run manager, and set user initializions: detector construction, physics list, and action
    auto *runManager = G4RunManagerFactory::CreateRunManager();
    runManager->SetUserInitialization(new DetectorConstruction(detectorConfig, plateThickness));
    runManager->SetUserInitialization(new PhysicsList());
    runManager->SetUserInitialization(new ActionInitialization(beamAngle, beamPMeV, beamParticleType, outputFile, outputFilePath));

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

    // Get pointer to UI manager and execute .mac file
    G4UImanager *UImanager = G4UImanager::GetUIpointer();
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