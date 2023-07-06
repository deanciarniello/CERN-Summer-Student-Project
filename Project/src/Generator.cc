#include "Generator.hh"

PrimaryGenerator::PrimaryGenerator(G4double beamAngle, G4double beamPMeV, G4String particleType) {
    // ========== Make Particle Gun ==========
    fParticleGun = new G4ParticleGun(1); //1 vertex per event

    // define particle type
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition *particle = particleTable->FindParticle(particleType); //muon

    // set the particle position and momentum direction on a circle in the xz plane
    G4double radius = 50.0 * cm;  // Set the desired radius
    G4double theta = beamAngle * deg;  // Set the desired angle
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
    fParticleGun->SetParticleMomentum(beamPMeV*MeV);
    fParticleGun->SetParticleDefinition(particle);
}

PrimaryGenerator::~PrimaryGenerator() {
    // ========== Delete Particle Gun ==========
    delete fParticleGun;
}

void PrimaryGenerator::GeneratePrimaries(G4Event *anEvent) {
    // ========== Generate Primary Vertex ==========
    fParticleGun->GeneratePrimaryVertex(anEvent);
} 