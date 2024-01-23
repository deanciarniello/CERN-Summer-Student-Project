/*
File: EventAction.hh
Author: Dean Ciarniello
Date: 2023-07-22
*/

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
    EventAction(RunAction* run);
    ~EventAction();

    virtual void BeginOfEventAction(const G4Event*);
    virtual void EndOfEventAction(const G4Event*);

    void SetPX(G4double px) { fPXout = px; }
    void SetPY(G4double py) { fPYout = py; }
    void SetPZ(G4double pz) { fPZout = pz; }
    void SetDepth(G4double depth) { fDepth = depth; }
    G4double GetDepth() { return fDepth; }
    
    void SetPlateTopHeight(G4double topHeight) { fPlateTopHeight = topHeight; }

    G4int GetPrimaryPDG() { return fPrimaryPDG; }

    void IncrementBoundaryCount() { fBoundaryCount += 1; }
    G4int GetBoundaryCount() { return fBoundaryCount; }

    G4bool GetIsDecayed() { return fIsDecayed; }
    void SetIsDecayed(G4bool isDecayed) { fIsDecayed = isDecayed; }

    G4bool GetIsAbsorbed() { return fIsAbsorbed; }
    void SetIsAbsorbed(G4bool isAbsorbed) { fIsAbsorbed = isAbsorbed; }

    G4bool GetHasEnteredMaterial() { return fHasEnteredMaterial; }
    void SetHasEnteredMaterial(G4bool hasEnteredMaterial) { fHasEnteredMaterial = hasEnteredMaterial; }

    G4int GetDecayPDG() { return fDecayPDG; }
    void SetDecayPDG( G4int decayPDG ) { fDecayPDG = decayPDG; }

private:
    G4double fPXout;
    G4double fPYout;
    G4double fPZout;
    G4double fPlateTopHeight;
    G4double fDepth;

    G4int fPrimaryPDG;
    G4int fDecayPDG;

    G4int fBoundaryCount;

    G4bool fHasEnteredMaterial;
    G4bool fIsDecayed;
    G4bool fIsAbsorbed;
};


#endif