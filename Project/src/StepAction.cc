#include "StepAction.hh"

StepAction::StepAction(EventAction *eventAction) {
    fEventAction = eventAction;
}

StepAction::~StepAction() {

}

void StepAction::UserSteppingAction(const G4Step *step) {
    G4int particlePDG = step->GetTrack()->GetDynamicParticle()->GetPDGcode();
    if (particlePDG == fEventAction->GetPrimaryPDG()) {

        G4bool isBoundary = step->IsLastStepInVolume();

        if (isBoundary) {
            fEventAction->IncrementBoundaryCount();
            if (fEventAction->GetBoundaryCount() == 2) {
                G4ThreeVector momentum = step->GetPostStepPoint()->GetMomentum();
                fEventAction->SetPX(momentum[0]);
                fEventAction->SetPY(momentum[1]);
                fEventAction->SetPZ(momentum[2]);
                G4cout << "End of boundary!!!" << G4endl;
            }
        }
        G4cout << "Is last step in boundary: " << isBoundary << G4endl;
    } else {
        fEventAction->SetIsDecayed(true);
    }
}
