#include "EventAction.hh"

EventAction::EventAction(RunAction*) {
    fPXout = 0;
    fPYout = 0;
    fPZout = 0;

    fPXin = 0;
    fPYin = 0;
    fPZin = 0;

    fXin = 0;
    fYin = 0;
    fXout = 0;
    fYout = 0;

    fIsDecayed = false;
    fIsTransmitted = false;
}

EventAction::~EventAction() {

}

void EventAction::BeginOfEventAction(const G4Event* event) {
    // ========== Set Event Action Parameters ==========
    fPXout = 0;
    fPYout = 0;
    fPZout = 0;
    
    //fBoundaryCount = 0;

    fIsDecayed = false;
    fIsTransmitted = false;


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
        SetIsTransmitted(true);
        //G4cout << "Absorbed!" << G4endl;
    }

    //if (fIsDecayed) { G4cout << "Decayed!" << G4endl; }

    // ========== Fill Ntuples/Histograms ==========
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->FillNtupleIColumn(2,0,event->GetEventID());
    man->FillNtupleIColumn(2,1,fIsDecayed);
    man->FillNtupleIColumn(2,2,fIsTransmitted);
    man->AddNtupleRow(2); 


    G4double theta_in = acos((fPZin)/sqrt(pow(fPXin,2) + pow(fPYin,2) + pow(fPZin,2)));
    G4double phi_in;
    if (fPZin > 0) {
        phi_in = acos(fPYin/sqrt(pow(fPXin,2) + pow(fPYin,2)));
    } else if (fPZin == 0) {
        phi_in = 0;
    } else {
        phi_in = -1*acos(fPYin/sqrt(pow(fPXin,2) + pow(fPYin,2))) + (2 * M_PI);
    }

    man->FillNtupleIColumn(0,0,event->GetEventID());
    man->FillNtupleDColumn(0,1,fXin);
    man->FillNtupleDColumn(0,2,fYin);
    man->FillNtupleDColumn(0,3,fPXin);
    man->FillNtupleDColumn(0,4,fPYin);
    man->FillNtupleDColumn(0,5,fPZin);
    man->FillNtupleDColumn(0,6,theta_in/deg);
    man->FillNtupleDColumn(0,7,phi_in/deg);
    man->FillNtupleDColumn(0,8,sqrt(pow(fPXin,2) + pow(fPYin,2) + pow(fPZin,2)));
    man->FillNtupleDColumn(0,9,sqrt(pow(fPXin,2) + pow(fPYin,2)));
    man->AddNtupleRow(0);

    man->FillH2(0, fXin, fYin);

    if (!fIsDecayed && !fIsTransmitted) {
        // Compute in and out angles
        G4double theta_out = acos((fPZout)/sqrt(pow(fPXout,2) + pow(fPYout,2) + pow(fPZout,2)));

        G4double phi_out;
        if (fPZout > 0) {
            phi_out = acos(fPYout/sqrt(pow(fPXout,2) + pow(fPYout,2)));
        } else if (fPZout == 0) {
            phi_out = 0;
        } else {
            phi_out = -1*acos(fPYout/sqrt(pow(fPXout,2) + pow(fPYout,2))) + (2 * M_PI);
        }

        man->FillNtupleIColumn(1,0,event->GetEventID());
        man->FillNtupleDColumn(1,1,fXout);
        man->FillNtupleDColumn(1,2,fYout);
        man->FillNtupleDColumn(1,3,fPXout);
        man->FillNtupleDColumn(1,4,fPYout);
        man->FillNtupleDColumn(1,5,fPZout);
        man->FillNtupleDColumn(1,6,theta_out/deg);
        man->FillNtupleDColumn(1,7,phi_out/deg);
        man->FillNtupleDColumn(1,8,sqrt(pow(fPXout,2) + pow(fPYout,2) + pow(fPZout,2)));
        man->FillNtupleDColumn(1,9,sqrt(pow(fPXout,2) + pow(fPYout,2)));
        man->AddNtupleRow(1);

        man->FillH2(1, fXout, fYout);
        man->FillH2(2, sqrt(pow(fPXin,2) + pow(fPYin,2) + pow(fPZin,2)), sqrt(pow(fPXout,2) + pow(fPYout,2) + pow(fPZout,2)));
        man->FillH2(3, theta_in/deg, theta_out/deg);
    }
}