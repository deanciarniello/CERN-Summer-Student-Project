#include "Action.hh"
#include "Generator.hh"

ActionInitialization::ActionInitialization() {

}

ActionInitialization::~ActionInitialization() {
    
}

void ActionInitialization::Build() const {
    PrimaryGenerator *generator = new PrimaryGenerator();
    SetUserAction(generator);

    RunAction *runAction = new RunAction();
    SetUserAction(runAction);

    EventAction *eventAction = new EventAction(runAction);
    SetUserAction(eventAction);

    StepAction *stepAction = new StepAction(eventAction);
    SetUserAction(stepAction);
}