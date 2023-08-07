#ifndef ACTION_HH
#define ACTION_HH

#include "G4VUserActionInitialization.hh"

#include "Generator.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "StepAction.hh"

class ActionInitialization : public G4VUserActionInitialization {
public:
    ActionInitialization(G4String, G4String);
    ~ActionInitialization();

    // Main function of program
    virtual void Build() const;

private:
    G4String fOutputFile;
    G4String fOutputPath;
};

#endif