#ifndef STEP_ACTION_HH
#define STEP_ACTION_HH

#include "G4UserSteppingAction.hh"
#include "G4Step.hh"
#include "G4Track.hh"

#include "DetectorConstruction.hh"
#include "EventAction.hh"

class StepAction : public G4UserSteppingAction {
public:
    StepAction(EventAction *eventAction);
    ~StepAction();

    virtual void UserSteppingAction(const G4Step*);

private:
    EventAction *fEventAction;
};

#endif