#ifndef ACTION_HH
#define ACTION_HH

#include "G4VUserActionInitialization.hh"

#include "Generator.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "StepAction.hh"

class ActionInitialization : public G4VUserActionInitialization {
public:
    ActionInitialization();
    ~ActionInitialization();

    // Main function of program
    virtual void Build() const;
};

#endif