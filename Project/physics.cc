#include "physics.hh"

PhysicsList::PhysicsList() {
    RegisterPhysics (new G4EmStandardPhysics());
    RegisterPhysics (new G4OpticalPhysics());
}

PhysicsList::~PhysicsList() {
    
}