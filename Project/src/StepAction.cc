#include "StepAction.hh"

StepAction::StepAction(EventAction *eventAction) {
    fEventAction = eventAction;
}

StepAction::~StepAction() {

}

void StepAction::UserSteppingAction(const G4Step *step) {
    // Check particle PDG
    G4int particlePDG = step->GetTrack()->GetDynamicParticle()->GetPDGcode();

    if (particlePDG == fEventAction->GetPrimaryPDG()) {

        // Check if step is last in current volume
        G4bool isBoundary = step->IsLastStepInVolume();

        if (isBoundary) {
            fEventAction->IncrementBoundaryCount();
            if (fEventAction->GetBoundaryCount() == 2) { // If particle is exiting plate (2nd volume it will leave)
                // Record particle momentum
                G4ThreeVector momentum = step->GetPostStepPoint()->GetMomentum();
                fEventAction->SetPX(momentum[0]);
                fEventAction->SetPY(momentum[1]);
                fEventAction->SetPZ(momentum[2]);
                //G4cout << "End of boundary!!!" << G4endl;
            }
        }
        //G4cout << "Is last step in boundary: " << isBoundary << G4endl;
    } else {
        // if PDG does not match primary particle, set IsDecayed boolean true
        fEventAction->SetIsDecayed(true);
    }
}
