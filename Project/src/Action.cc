#include "Action.hh"
#include "Generator.hh"

ActionInitialization::ActionInitialization(G4double angle, G4double p, G4String particle, G4String output) {
    fBeamAngle = angle;
    fBeamPMeV = p;
    fBeamParticleType = particle;
    fOutputFile = output;
}

ActionInitialization::~ActionInitialization() {
    
}

void ActionInitialization::Build() const {
    // ========== Set All User Actions ==========
    PrimaryGenerator *generator = new PrimaryGenerator(fBeamAngle, fBeamPMeV, fBeamParticleType);
    SetUserAction(generator);

    RunAction *runAction = new RunAction(fOutputFile);
    SetUserAction(runAction);

    EventAction *eventAction = new EventAction(runAction);
    SetUserAction(eventAction);

    StepAction *stepAction = new StepAction(eventAction);
    SetUserAction(stepAction);
}