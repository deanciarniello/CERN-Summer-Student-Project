/*
File: Action.cc
Author: Dean Ciarniello
Date: 2023-08-09
*/

// Includes
// ===================================================
#include "Action.hh"
#include "Generator.hh"

// ActionInitialization Constructor
// ===================================================
ActionInitialization::ActionInitialization(G4String output, G4String outputPath) {
    fOutputFile = output;
    fOutputPath = outputPath;
}

// ActionInitialization Destructor
// ===================================================
ActionInitialization::~ActionInitialization() {
    
}

// ActionInitialization Build
// Info: constructs and sets all user actions
// ===================================================
void ActionInitialization::Build() const {
    PrimaryGenerator *generator = new PrimaryGenerator();
    SetUserAction(generator);

    RunAction *runAction = new RunAction(fOutputFile, fOutputPath);
    SetUserAction(runAction);

    EventAction *eventAction = new EventAction(runAction);
    SetUserAction(eventAction);

    StepAction *stepAction = new StepAction(eventAction);
    SetUserAction(stepAction);
}