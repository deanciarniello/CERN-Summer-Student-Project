#include "generator.hh"

PrimaryGenerator::PrimaryGenerator() {
    fParticleGun = new G4ParticleGun(1); //1 vertex per event
}

PrimaryGenerator::~PrimaryGenerator() {
    delete fParticleGun;
}

void PrimaryGenerator::GeneratePrimaries(G4Event *anEvent) {
    // define particle type
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition *particle = particleTable->FindParticle("mu-"); //muon

    
    // set the particle position and momentum direction on a circle in the xz plane
    G4double radius = 50.0 * cm;  // Set the desired radius
    G4double phi = 85.0 * deg;  // Set the desired angle

    // calculate the position on the circle
    G4double x = 0.0;
    G4double y = radius * std::cos(phi);
    G4double z = radius * std::sin(phi);
    fParticleGun->SetParticlePosition(G4ThreeVector(x, y, z));

    // set the particle momentum direction to point towards the origin
    G4double px = -x;
    G4double py = -y;
    G4double pz = -z;
    fParticleGun->SetParticleMomentumDirection(G4ThreeVector(px, py, pz));

    // set other beam parameters
    fParticleGun->SetParticleMomentum(75.*MeV);
    fParticleGun->SetParticleDefinition(particle);

    fParticleGun->GeneratePrimaryVertex(anEvent);
}