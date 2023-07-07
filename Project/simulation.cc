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

int main(int argc, char** argv) {
    // argv:
    // 1) .mac file
    // 2) detector config (plate material)
    // 3) beam angle (w.r.t normal)
    // 4) beam momentum
    // 5) beam particle type
    // 6) output .root file name
    G4int detectorConfig = std::stoi(argv[2]);
    G4double beamAngle = std::stod(argv[3]);
    G4double beamPMeV = std::stod(argv[4]);
    G4String beamParticleType = argv[5];
    G4String outputFile = argv[6];

    auto *runManager = G4RunManagerFactory::CreateRunManager();
    runManager->SetUserInitialization(new DetectorConstruction(detectorConfig));
    runManager->SetUserInitialization(new PhysicsList());
    runManager->SetUserInitialization(new ActionInitialization(beamAngle, beamPMeV, beamParticleType, outputFile));

    runManager->Initialize();

    G4UIExecutive *ui = new G4UIExecutive(argc, argv);

    G4VisManager *visManager = new G4VisExecutive();
    visManager->Initialize();

    G4UImanager *UImanager = G4UImanager::GetUIpointer();

    G4String command = "/control/execute ";
    G4String fileName = argv[1];
    UImanager->ApplyCommand(command+fileName);
    
    //ui->SessionStart();

    delete visManager;
    delete runManager;
    delete ui;

    return 0;
}