#include "physics.hh"

PhysicsList::PhysicsList() {
    RegisterPhysics (new G4EmStandardPhysics());
    RegisterPhysics (new G4EmExtraPhysics());
    RegisterPhysics (new G4DecayPhysics());
    RegisterPhysics (new G4HadronElasticPhysics());
    RegisterPhysics (new G4IonPhysics());
    RegisterPhysics (new G4OpticalPhysics());
}

PhysicsList::~PhysicsList() {
    
}