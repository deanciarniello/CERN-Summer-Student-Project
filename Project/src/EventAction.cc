/*
File: EventAction.cc
Author: Dean Ciarniello
Date: 2023-07-22
*/

// Includes
// ===================================================
#include "EventAction.hh"

// EventAction Constructor
// ===================================================
EventAction::EventAction(RunAction*) {
    // Initialize Event Parameters
    fPXout = 0;
    fPYout = 0;
    fPZout = 0;
    
    fDecayPDG = 0;

    fIsDecayed = false;
    fIsAbsorbed = false;
}

// EventAction Destructor
// ===================================================
EventAction::~EventAction() {

}

// EventAction BeginOfEvent Action
// Info: set/reset all event variables
// ===================================================
void EventAction::BeginOfEventAction(const G4Event* event) {
    fPXout = 0;
    fPYout = 0;
    fPZout = 0;

    fDecayPDG = 0;

    fIsDecayed = false;
    fIsAbsorbed = false;

    fPrimaryPDG = event->GetPrimaryVertex()->GetPrimary()->GetPDGcode();
}

// EventAction EndOfEventAction
// Info: record all event variables in corresponding root ntuples
// ===================================================
void EventAction::EndOfEventAction(const G4Event* event) {
    /*G4cout << "End of event action." << G4endl;
    G4cout << "Px: " << fPXout << G4endl;
    G4cout << "Py: " << fPYout << G4endl;
    G4cout << "Pz: " << fPZout << G4endl;*/

    
    //G4cout << "Secondary PDGs before ntuple: "<< fSecondaryPDG.size() << G4endl;

    // Check if particle absorbed
    G4double Pabs = sqrt(pow(fPXout,2) + pow(fPYout,2) + pow(fPZout,2));
    if (Pabs == 0) {
        SetIsAbsorbed(true);
        //G4cout << "Absorbed!" << G4endl;
    }
    //if (fIsDecayed) { G4cout << "Decayed!" << G4endl; }

    // ========== Fill Ntuples/Histograms ==========
    G4AnalysisManager *man = G4AnalysisManager::Instance();

    G4bool isDecayedIn = ((!fHasEnteredMaterial) && fIsDecayed);
    G4bool isDecayedDuring = ((fHasEnteredMaterial && fIsDecayed) && fIsAbsorbed);
    G4bool isDecayedOut = ((fHasEnteredMaterial && fIsDecayed) && (!fIsAbsorbed));

    // Fill All Event ntuples
    man->FillNtupleIColumn(1,0,event->GetEventID());
    man->FillNtupleIColumn(1,1,fIsDecayed);
    man->FillNtupleIColumn(1,2,fIsAbsorbed);
    man->FillNtupleIColumn(1,3,isDecayedIn);
    man->FillNtupleIColumn(1,4,isDecayedDuring);
    man->FillNtupleIColumn(1,5,isDecayedOut);
    man->FillNtupleIColumn(1,6,fDecayPDG);
    man->AddNtupleRow(1); 

    if ((!isDecayedIn) && (!isDecayedDuring) && (!fIsAbsorbed)) {
        // Compute theta
        double theta = acos((fPYout)/sqrt(pow(fPXout,2) + pow(fPYout,2) + pow(fPZout,2)));

        // Compute phi
        double phi;
        if (fPXout > 0) {
            phi = acos(fPZout/sqrt(pow(fPXout,2) + pow(fPZout,2)));
        } else if (fPXout == 0) {
            phi = 0;
        } else {
            phi = -1*acos(fPZout/sqrt(pow(fPXout,2) + pow(fPZout,2))) + (2 * M_PI);
        }

        // Fill PrimaryEvent ntuples
        man->FillNtupleIColumn(0,0,event->GetEventID());
        man->FillNtupleDColumn(0,1,fPXout);
        man->FillNtupleDColumn(0,2,fPYout);
        man->FillNtupleDColumn(0,3,fPZout);
        man->FillNtupleDColumn(0,4,theta/deg);
        man->FillNtupleDColumn(0,5,phi/deg);
        man->AddNtupleRow(0);
    }
}