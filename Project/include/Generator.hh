/*
File: Generator.hh
Author: Dean Ciarniello
Date: 2023-07-22
*/

#ifndef GENERATOR_HH
#define GENERATOR_HH

#include <cmath>

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4ParticleGun.hh"
#include "G4SystemOfUnits.hh"
#include "G4ParticleTable.hh"
#include "G4GeneralParticleSource.hh"

class PrimaryGenerator : public G4VUserPrimaryGeneratorAction {
public:
    PrimaryGenerator(G4double, G4double, G4String);
    ~PrimaryGenerator();
    virtual void GeneratePrimaries(G4Event*);

private:
    G4ParticleGun *fParticleGun;
};

#endif