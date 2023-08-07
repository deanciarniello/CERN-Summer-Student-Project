#include "PhysicsList.hh"

PhysicsList::PhysicsList() {
    RegisterPhysics (new G4EmStandardPhysics_option4());
    RegisterPhysics (new G4DecayPhysics());

    RegisterPhysics(new G4StepLimiterPhysics());
}

PhysicsList::~PhysicsList() {
    
}