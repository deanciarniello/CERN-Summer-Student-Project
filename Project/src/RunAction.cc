#include "RunAction.hh"

RunAction::RunAction(G4String output) {
    fOutputFile = output;
}

RunAction::~RunAction() {

}

void RunAction::BeginOfRunAction(const G4Run* run) {
    // =========== Create Ntuples and Histograms in .root file ==========
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->OpenFile(fOutputFile);

    // Create Ntuple for Primary Events (no decay)
    man->CreateNtuple("PrimaryEvents", "Primary Events");  // can rename as appropriate
    man->CreateNtupleIColumn("fEvent"); //I/D correspond to integer/double
    man->CreateNtupleDColumn("fPx");
    man->CreateNtupleDColumn("fPy");
    man->CreateNtupleDColumn("fPz");
    man->CreateNtupleDColumn("fTheta");
    man->CreateNtupleDColumn("fPhi");
    man->FinishNtuple();

    // Create Ntuple for All Events (including decay events)
    man->CreateNtuple("AllEvents", "All Events");
    man->CreateNtupleIColumn("fEvent");
    man->CreateNtupleIColumn("fIsDecayed");
    man->CreateNtupleIColumn("fIsAbsorbed");
    man->FinishNtuple();

    // Create 2D Histograms
    man->CreateH2("Phi_vs_Theta", "Phi versus Theta", 5, 0., 360., 5, 0., 180.);
    man->CreateH2("Pz_vs_Theta", "Pz versus Theta", 2.5, 0., 100., 5, 0., 180.);
}

void RunAction::EndOfRunAction(const G4Run*) {
    // ========== Write and Close .root file ==========
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->Write();
    man->CloseFile();
}