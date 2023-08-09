/*
File: StepAction.cc
Author: Dean Ciarniello
Date: 2023-07-22
*/

// Includes
// ===================================================
#include "StepAction.hh"


// StepAction Constructor
// ===================================================
StepAction::StepAction(EventAction *eventAction) {
    fEventAction = eventAction;
}

// StepAction Destructor
// ===================================================
StepAction::~StepAction() {

}

// StepAction UserSteppingAction
// Info: follow the steps/tracks of simulated particles, record whether they decay
//       or ar absorbed in the plate volume, and set event variables
//       such as momentum, when the particle has left the scattering plate volume
void StepAction::UserSteppingAction(const G4Step *step) {
    // Check particle PDG
    G4int particlePDG = step->GetTrack()->GetDynamicParticle()->GetPDGcode();

    if (particlePDG == fEventAction->GetPrimaryPDG()) {
        // Check if step is last in current volume
        G4bool isBoundary = step->IsLastStepInVolume();
        
        if (isBoundary) {
            //fEventAction->IncrementBoundaryCount();

            if (step->GetTrack()->GetNextVolume()) {
                //G4cout << "Next Volume: " << step->GetTrack()->GetNextVolume()->GetName() << G4endl;

                if (step->GetTrack()->GetNextVolume()->GetName() == "physWorld") {
                    // Record particle momentum
                    G4ThreeVector momentum = step->GetPostStepPoint()->GetMomentum();
                    fEventAction->SetPX(momentum[0]);
                    fEventAction->SetPY(momentum[1]);
                    fEventAction->SetPZ(momentum[2]);
                    //G4cout << "End of boundary!!!" << G4endl;
                }
            }
        }
        //G4cout << "Is last step in boundary: " << isBoundary << G4endl;
    } else {
        // if PDG does not match primary particle, set IsDecayed boolean true
        fEventAction->SetIsDecayed(true);
    }
}
