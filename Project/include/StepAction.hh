/*
File: StepAction.hh
Author: Dean Ciarniello
Date: 2023-07-22
*/

#ifndef STEP_ACTION_HH
#define STEP_ACTION_HH

#include "G4UserSteppingAction.hh"
#include "G4Step.hh"
#include "G4Track.hh"
#include "G4LogicalVolume.hh"

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