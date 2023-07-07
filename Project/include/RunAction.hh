#ifndef RUN_ACTION_HH
#define RUN_ACTION_HH

#include "G4UserRunAction.hh"
#include "g4root.hh"

#include <filesystem>

class RunAction : public G4UserRunAction {
public:
    RunAction(const G4String);
    ~RunAction();

    virtual void BeginOfRunAction(const G4Run*);
    virtual void EndOfRunAction(const G4Run*);

private:
    G4String fOutputFile;
};

#endif