#include "EventAction.hh"

EventAction::EventAction(RunAction*) {
    fPXout = 0;
    fPYout = 0;
    fPZout = 0;
    
    fBoundaryCount = 0;

    fIsDecayed = false;
    fIsAbsorbed = false;
}

EventAction::~EventAction() {

}

void EventAction::BeginOfEventAction(const G4Event* event) {
    // ========== Set Event Action Parameters ==========
    fPXout = 0;
    fPYout = 0;
    fPZout = 0;
    
    fBoundaryCount = 0;

    fIsDecayed = false;
    fIsAbsorbed = false;


    fPrimaryPDG = event->GetPrimaryVertex()->GetPrimary()->GetPDGcode();
}

void EventAction::EndOfEventAction(const G4Event* event) {
    // ========== Print Out Final Event Momenta for Primary Particle ==========
    /*G4cout << "End of event action." << G4endl;
    G4cout << "Px: " << fPXout << G4endl;
    G4cout << "Py: " << fPYout << G4endl;
    G4cout << "Pz: " << fPZout << G4endl;*/
    G4double Pabs = sqrt(pow(fPXout,2) + pow(fPYout,2) + pow(fPZout,2));
    if (Pabs == 0) {
        SetIsAbsorbed(true);
    }

    // ========== Fill Ntuples/Histograms ==========
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->FillNtupleIColumn(1,0,event->GetEventID());
    man->FillNtupleIColumn(1,1,fIsDecayed);
    man->FillNtupleIColumn(1,2,fIsAbsorbed);
    man->AddNtupleRow(1); 

    if ((!fIsDecayed) && (!fIsAbsorbed)) {
        double theta = acos((fPYout)/sqrt(pow(fPXout,2) + pow(fPYout,2) + pow(fPZout,2)));

        double phi;
        if (fPXout > 0) {
            phi = acos(fPZout/sqrt(pow(fPXout,2) + pow(fPZout,2)));
        } else if (fPXout == 0) {
            phi = 0;
        } else {
            phi = -1*acos(fPZout/sqrt(pow(fPXout,2) + pow(fPZout,2))) + (2 * M_PI);
        }
        man->FillNtupleIColumn(0,0,event->GetEventID());
        man->FillNtupleDColumn(0,1,fPXout);
        man->FillNtupleDColumn(0,2,fPYout);
        man->FillNtupleDColumn(0,3,fPZout);
        man->FillNtupleDColumn(0,4,theta/deg);
        man->FillNtupleDColumn(0,5,phi/deg);
        man->AddNtupleRow(0);

        man->FillH2(0, phi/deg, theta/deg);
        man->FillH2(1, fPZout, theta/deg);
    }
}