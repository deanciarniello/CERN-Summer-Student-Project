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
// ===================================================
// Info: follow the steps/tracks of simulated particles, record whether they decay
//       or ar absorbed in the plate volume, and set event variables
//       such as momentum, when the particle has left the scattering plate volume
void StepAction::UserSteppingAction(const G4Step *step) {
    // Get particle PDG and current volume
    G4int particlePDG = step->GetTrack()->GetDynamicParticle()->GetPDGcode();
    G4String currentVolume = step->GetTrack()->GetVolume()->GetName();

    // Set has entered material if particle is interacting with plate for the first time
    if ((currentVolume == "physPlate") || (currentVolume == "physCoatingGold") || (!(fEventAction->GetHasEnteredMaterial()))) {
        fEventAction->SetHasEnteredMaterial(true);
    }

    // Check if particle has not decayed
    if (particlePDG == fEventAction->GetPrimaryPDG() && !(fEventAction->GetIsDecayed())) {
        // Check if step is last in current volume and there is another volume (i.e. not the end of the world)

        if (step->IsLastStepInVolume() && step->GetTrack()->GetNextVolume()) {
            // If step is into world (i.e. out of plate/coating), record momentum
            if (step->GetTrack()->GetNextVolume()->GetName() == "physWorld") {
                // Record particle momentum
                G4ThreeVector momentum = step->GetPostStepPoint()->GetMomentum();
                fEventAction->SetPX(momentum[0]);
                fEventAction->SetPY(momentum[1]);
                fEventAction->SetPZ(momentum[2]);
                //G4cout << "End of boundary!!!" << G4endl;
            }
        }

    } else {
        // If in plate or plate coating, set absorbed true
        if ((step->GetTrack()->GetVolume()->GetName() != "physWorld")) {
            fEventAction->SetIsAbsorbed(true);
        }
        // Set decayed to true and record decay pdg
        if (!fEventAction->GetIsDecayed()) {
            fEventAction->SetIsDecayed(true);
            fEventAction->SetDecayPDG(particlePDG);
        }
    }
}
