/*
File: PhysicsList.hh
Author: Dean Ciarniello
Date: 2023-07-22
*/

#ifndef PHYSICS_HH 
#define PHYSICS_HH

#include "G4VModularPhysicsList.hh"
#include "G4EmStandardPhysics.hh"
#include "G4DecayPhysics.hh"
#include "G4EmStandardPhysics_option4.hh"
#include "G4StepLimiterPhysics.hh"

class PhysicsList : public G4VModularPhysicsList {
public:
    PhysicsList();
    ~PhysicsList();
};


#endif