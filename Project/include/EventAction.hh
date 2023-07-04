#ifndef EVENT_ACTION_HH
#define EVENT_ACTION_HH

#include <cmath>

#include "G4UserEventAction.hh"
#include "G4Event.hh"
#include "G4SystemOfUnits.hh"

#include "g4root.hh"

#include "RunAction.hh"

class EventAction : public G4UserEventAction {
public:
    EventAction(RunAction*);
    ~EventAction();

    virtual void BeginOfEventAction(const G4Event*);
    virtual void EndOfEventAction(const G4Event*);

    void SetPX(G4double px) { fPXout = px; }
    void SetPY(G4double py) { fPYout = py; }
    void SetPZ(G4double pz) { fPZout = pz; }

    //void SetPrimaryPDG(G4int pdg) { fPrimaryPDG = pdg; }
    G4int GetPrimaryPDG() { return fPrimaryPDG; }

    void IncrementBoundaryCount() { fBoundaryCount += 1; }
    G4int GetBoundaryCount() { return fBoundaryCount; }

    G4bool GetIsDecayed() { return fIsDecayed; }
    void SetIsDecayed(G4bool isDecayed) { fIsDecayed = isDecayed; }

private:
    G4double fPXout;
    G4double fPYout;
    G4double fPZout;

    G4int fPrimaryPDG;

    G4int fBoundaryCount;

    G4bool fIsDecayed;
};


#endif