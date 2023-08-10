/*
File: PhysicsList.cc
Author: Dean Ciarniello
Date: 2023-08-04
*/

// Includes
// ===================================================
#include "PhysicsList.hh"

// PhysicsList Constructor
// Info: add EM physics (option 4), decay physics, and step limiter (to adjust step size in volumes)
// ===================================================
PhysicsList::PhysicsList() {
    RegisterPhysics (new G4EmStandardPhysics_option4());
    RegisterPhysics (new G4DecayPhysics());

    RegisterPhysics(new G4StepLimiterPhysics());
}

// PhysicsList Destructor
// ===================================================
PhysicsList::~PhysicsList() {
    
}