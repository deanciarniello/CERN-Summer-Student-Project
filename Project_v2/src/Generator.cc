/*
File: Generator.cc
Author: Dean Ciarniello
Date: 2023-07-22
*/

// Includes
// ===================================================
#include "Generator.hh"

// PrimaryGenerator Constructor
// ===================================================
PrimaryGenerator::PrimaryGenerator() {
    // Use a general particle source
    fParticleSource = new G4GeneralParticleSource();
}

// PrimaryGenerator Destructor
// ===================================================
PrimaryGenerator::~PrimaryGenerator() {
    delete fParticleSource;
}

// PrimaryGenerator GeneratePrimaryes
// ===================================================
void PrimaryGenerator::GeneratePrimaries(G4Event *anEvent) {
    // Generate one event
    fParticleSource->GeneratePrimaryVertex(anEvent);
} 