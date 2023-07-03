#include "StepAction.hh"

StepAction::StepAction(EventAction *eventAction) {
    fEventAction = eventAction;
}

StepAction::~StepAction() {

}

void StepAction::UserSteppingAction(const G4Step *step) {
    G4bool isBoundary = step->IsLastStepInVolume();
    G4StepPoint *postStep = step->GetPostStepPoint();

    if (isBoundary) {
        fEventAction->IncrementBoundaryCount();
        G4int boundaryCount = fEventAction->GetBoundaryCount();
        if (boundaryCount == 2) {
            G4ThreeVector momentum = postStep->GetMomentum();
            fEventAction->SetPX(momentum[0]);
            fEventAction->SetPY(momentum[1]);
            fEventAction->SetPZ(momentum[2]);
            G4cout << "End of boundary!!!" << G4endl;
        }
    }
    G4cout << "Is last step in boundary: " << isBoundary << G4endl;
}
