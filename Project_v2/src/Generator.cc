#include "Generator.hh"

PrimaryGenerator::PrimaryGenerator() {
   fParticleSource = new G4GeneralParticleSource();
}

PrimaryGenerator::~PrimaryGenerator() {
    // ========== Delete Particle Gun ==========
    delete fParticleSource;
}

void PrimaryGenerator::GeneratePrimaries(G4Event *anEvent) {
    // ========== Generate Primary Vertex ==========
    fParticleSource->GeneratePrimaryVertex(anEvent);
} 