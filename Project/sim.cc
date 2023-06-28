#include <iostream>

#include "G4RunManagerFactory.hh"
#include "G4UImanager.hh"
#include "G4VisManager.hh"
#include "G4UIExecutive.hh"
#include "G4VisExecutive.hh"

#include "construction.hh"
#include "physics.hh"
#include "action.hh"

int main(int argc, char** argv) {
    auto *runManager = G4RunManagerFactory::CreateRunManager();;
    runManager->SetUserInitialization(new DetectorConstruction());
    runManager->SetUserInitialization(new PhysicsList());
    runManager->SetUserInitialization(new ActionInitialization());

    runManager->Initialize();

    G4UIExecutive *ui = new G4UIExecutive(argc, argv);

    G4VisManager *visManager = new G4VisExecutive();
    visManager->Initialize();

    G4UImanager *UImanager = G4UImanager::GetUIpointer();

    UImanager->ApplyCommand("/vis/open OGLI ");
    UImanager->ApplyCommand("/vis/viewer/set/viewpointVector 1 1 1");
    UImanager->ApplyCommand("/vis/drawVolume ");
    UImanager->ApplyCommand("/vis/viewer/set/autoRefresh true");

    UImanager->ApplyCommand("/vis/scene/add/trajectories smooth");
    UImanager->ApplyCommand("/vis/geometry/set/lineWidth all 2");

    ui->SessionStart();

    delete visManager;
    delete runManager;
    delete ui;

    return 0;
}