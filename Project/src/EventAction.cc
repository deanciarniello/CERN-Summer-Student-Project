#include "EventAction.hh"

EventAction::EventAction(RunAction*) {
    fPXout = 0;
    fPYout = 0;
    fPZout = 0;
    
    fBoundaryCount = 0;
}

EventAction::~EventAction() {

}

void EventAction::BeginOfEventAction(const G4Event*) {
    fPXout = 0;
    fPYout = 0;
    fPZout = 0;
    
    fBoundaryCount = 0;
}

void EventAction::EndOfEventAction(const G4Event* event) {
    G4cout << "End of event action." << G4endl;
    G4cout << "Px: " << fPXout << G4endl;
    G4cout << "Py: " << fPYout << G4endl;
    G4cout << "Pz: " << fPZout << G4endl;

    double theta = acos((fPZout)/sqrt(pow(fPXout,2) + pow(fPYout,2) + pow(fPZout,2)));

    double phi;
    if (fPYout > 0) {
        phi = acos(fPXout/sqrt(pow(fPXout,2) + pow(fPYout,2)));
    } else if (fPYout == 0) {
        phi = 0;
    } else {
        phi = -1*acos(fPXout/sqrt(pow(fPXout,2) + pow(fPYout,2)));
    }

    G4AnalysisManager *man = G4AnalysisManager::Instance();

    man->FillNtupleIColumn(0,event->GetEventID());
    man->FillNtupleDColumn(1,fPXout);
    man->FillNtupleDColumn(2,fPYout);
    man->FillNtupleDColumn(3,fPZout);
    man->FillNtupleDColumn(4,theta/deg);
    man->FillNtupleDColumn(5,phi/deg);
    man->AddNtupleRow(); 

    man->FillH2(0, phi/deg, theta/deg);
}