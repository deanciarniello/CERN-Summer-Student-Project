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

    void SetPXout(G4double px) { fPXout = px; }
    void SetPYout(G4double py) { fPYout = py; }
    void SetPZout(G4double pz) { fPZout = pz; }

    void SetPXin(G4double px) { fPXin = px; }
    void SetPYin(G4double py) { fPYin = py; }
    void SetPZin(G4double pz) { fPZin = pz; }

    void SetXin(G4double x) { fXin = x; }
    void SetYin(G4double y) { fYin = y; }

    void SetXout(G4double x) { fXout = x; }
    void SetYout(G4double y) { fYout = y; }

    G4int GetPrimaryPDG() { return fPrimaryPDG; }

    G4bool GetIsDecayed() { return fIsDecayed; }
    void SetIsDecayed(G4bool isDecayed) { fIsDecayed = isDecayed; }

    void SetIsTransmitted(G4bool isTransmitted) { fIsTransmitted = isTransmitted; }

private:
    G4double fPXout;
    G4double fPYout;
    G4double fPZout;

    G4double fPXin;
    G4double fPYin;
    G4double fPZin;

    G4double fXout;
    G4double fYout;
    G4double fXin;
    G4double fYin;

    G4int fPrimaryPDG;

    G4bool fIsDecayed;
    G4bool fIsTransmitted;
};


#endif