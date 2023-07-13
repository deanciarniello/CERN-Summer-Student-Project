#ifndef ACTION_HH
#define ACTION_HH

#include "G4VUserActionInitialization.hh"

#include "Generator.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "StepAction.hh"

class ActionInitialization : public G4VUserActionInitialization {
public:
    ActionInitialization(const G4double, const G4double, const G4String, const G4String, const G4String);
    ~ActionInitialization();

    // Main function of program
    virtual void Build() const;

private:
    G4double fBeamAngle;
    G4double fBeamPMeV;
    G4String fBeamParticleType;
    G4String fOutputFile;
    G4String fOutputPath;
};

#endif