#include "Generator.hh"

PrimaryGenerator::PrimaryGenerator() {
    fParticleGun = new G4ParticleGun(1); //1 vertex per event

    // define particle type
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition *particle = particleTable->FindParticle("mu-"); //muon

    // set the particle position and momentum direction on a circle in the xz plane
    G4double radius = 50.0 * cm;  // Set the desired radius
    G4double theta = 88.5 * deg;  // Set the desired angle
    G4double phi = 0. * deg;

    // calculate the position on the circle
    G4double z = radius * cos(phi) * sin(theta);
    G4double x = radius * sin(phi) * sin(theta);
    G4double y = radius * cos(theta);
    fParticleGun->SetParticlePosition(G4ThreeVector(x, y, z));

    // set the particle momentum direction to point towards the origin
    G4double px = -x;
    G4double py = -y;
    G4double pz = -z;
    fParticleGun->SetParticleMomentumDirection(G4ThreeVector(px, py, pz));

    // set other beam parameters
    fParticleGun->SetParticleMomentum(90.*MeV);
    fParticleGun->SetParticleDefinition(particle);
}

PrimaryGenerator::~PrimaryGenerator() {
    delete fParticleGun;
}

void PrimaryGenerator::GeneratePrimaries(G4Event *anEvent) {
    fParticleGun->GeneratePrimaryVertex(anEvent);
}