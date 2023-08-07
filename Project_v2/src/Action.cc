#include "Action.hh"
#include "Generator.hh"

ActionInitialization::ActionInitialization(G4String output, G4String outputPath) {
    fOutputFile = output;
    fOutputPath = outputPath;
}

ActionInitialization::~ActionInitialization() {
    
}

void ActionInitialization::Build() const {
    // ========== Set All User Actions ==========
    PrimaryGenerator *generator = new PrimaryGenerator();
    SetUserAction(generator);

    RunAction *runAction = new RunAction(fOutputFile, fOutputPath);
    SetUserAction(runAction);

    EventAction *eventAction = new EventAction(runAction);
    SetUserAction(eventAction);

    StepAction *stepAction = new StepAction(eventAction);
    SetUserAction(stepAction);
}