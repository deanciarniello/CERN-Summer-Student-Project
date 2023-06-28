#include "action.hh"
#include "generator.hh"

ActionInitialization::ActionInitialization() {

}

ActionInitialization::~ActionInitialization() {
    
}

void ActionInitialization::Build() const {
    PrimaryGenerator *generator = new PrimaryGenerator();
    SetUserAction(generator);
}