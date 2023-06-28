#include "generator.hh"

PrimaryGenerator::PrimaryGenerator() {
    fParticleGun = new G4ParticleGun(1); //1 vertex per event
}

PrimaryGenerator::~PrimaryGenerator() {
    delete fParticleGun;
}

void PrimaryGenerator::GeneratePrimaries(G4Event *anEvent) {
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    G4String particleName="proton";
    G4ParticleDefinition *particle = particleTable->FindParticle("proton");

    G4ThreeVector pos(0.,0.,0.);
    G4ThreeVector mom(0.,0.,1.);

    fParticleGun->SetParticlePosition(pos);
    fParticleGun->SetParticleMomentumDirection(mom);
    fParticleGun->SetParticleMomentum(100.*GeV);
    fParticleGun->SetParticleDefinition(particle);

    fParticleGun->GeneratePrimaryVertex(anEvent);
}