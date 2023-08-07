#include "StepAction.hh"

StepAction::StepAction(EventAction *eventAction) {
    fEventAction = eventAction;
}

StepAction::~StepAction() {

}

void StepAction::UserSteppingAction(const G4Step *step) {
    // Check particle PDG
    G4int particlePDG = step->GetTrack()->GetDynamicParticle()->GetPDGcode();

    // If particle has not decayed
    if (particlePDG == fEventAction->GetPrimaryPDG()) {
        // If particle is about to exit current volume
        if (step->IsLastStepInVolume()) {
            //G4cout << step->GetTrack()->GetVolume()->GetName() << G4endl;
            
            // If particle is about to exit capillary
            if ((step->GetTrack()->GetVolume()->GetName() == "physEndCap") && (step->GetTrack()->GetNextVolume()->GetName() == "physWorld") && (step->GetPostStepPoint()->GetMomentum()[2] < 0)) {
                // Record particle momentum
                G4ThreeVector momentum = step->GetPostStepPoint()->GetMomentum();
                fEventAction->SetPXout(momentum[0]);
                fEventAction->SetPYout(momentum[1]);
                fEventAction->SetPZout(momentum[2]);

                G4ThreeVector position = step->GetPostStepPoint()->GetPosition();
                fEventAction->SetXout(position[0]);
                fEventAction->SetYout(position[1]);
                //G4cout << "End of boundary!!!" << G4endl;
            } else if ((step->GetTrack()->GetVolume()->GetName() == "physStartCap") && (step->GetTrack()->GetNextVolume()->GetName() == "physWorld") && (step->GetPostStepPoint()->GetMomentum()[2] < 0)) {
                // Record particle momentum
                G4ThreeVector momentum = step->GetPostStepPoint()->GetMomentum();
                fEventAction->SetPXin(momentum[0]);
                fEventAction->SetPYin(momentum[1]);
                fEventAction->SetPZin(momentum[2]);

                G4ThreeVector position = step->GetPostStepPoint()->GetPosition();
                fEventAction->SetXin(position[0]);
                fEventAction->SetYin(position[1]);
            }
        }
        //G4cout << "Is last step in boundary: " << isBoundary << G4endl;
    } else {
        // if PDG does not match primary particle, set IsDecayed boolean true
        fEventAction->SetIsDecayed(true);
    }
}
