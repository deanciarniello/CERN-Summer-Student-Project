#include "RunAction.hh"

RunAction::RunAction() {

}

RunAction::~RunAction() {

}

void RunAction::BeginOfRunAction(const G4Run* run) {
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->OpenFile("output.root");

    man->CreateNtuple("Simulation", "Output");  // can rename as appropriate
    man->CreateNtupleIColumn("fEvent"); //I/D correspond to integer/double
    man->CreateNtupleDColumn("fPx");
    man->CreateNtupleDColumn("fPy");
    man->CreateNtupleDColumn("fPz");
    man->CreateNtupleDColumn("fTheta");
    man->CreateNtupleDColumn("fPhi");
    man->FinishNtuple();
    
    man->CreateH2("Phi_vs_Theta", "Phi versus Theta", 5, 0., 360., 5, 0., 180.);
}

void RunAction::EndOfRunAction(const G4Run*) {
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->Write();
    man->CloseFile();
}