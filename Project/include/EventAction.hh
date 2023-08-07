#ifndef EVENT_ACTION_HH
#define EVENT_ACTION_HH

#include <cmath>

#include "G4UserEventAction.hh"
#include "G4Event.hh"
#include "G4SystemOfUnits.hh"

//#include "G4AnalysisManager.hh"
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

    G4int GetPrimaryPDG() { return fPrimaryPDG; }

    void IncrementBoundaryCount() { fBoundaryCount += 1; }
    G4int GetBoundaryCount() { return fBoundaryCount; }

    G4bool GetIsDecayed() { return fIsDecayed; }
    void SetIsDecayed(G4bool isDecayed) { fIsDecayed = isDecayed; }

    G4bool GetIsAbsorbed() { return fIsAbsorbed; }
    void SetIsAbsorbed(G4bool isAbsorbed) { fIsAbsorbed = isAbsorbed; }

private:
    G4double fPXout;
    G4double fPYout;
    G4double fPZout;

    G4int fPrimaryPDG;

    G4int fBoundaryCount;

    G4bool fIsDecayed;
    G4bool fIsAbsorbed;
};


#endif