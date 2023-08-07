#include "RunAction.hh"

RunAction::RunAction(G4String output, G4String outputPath) {
    fOutputFile = output;
    fOutputPath = outputPath;
}

RunAction::~RunAction() {

}

void RunAction::BeginOfRunAction(const G4Run*) {
    // =========== Create Ntuples and Histograms in .root file ==========
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->OpenFile(fOutputPath+fOutputFile);

    // Create Ntuple for Input Events
    man->CreateNtuple("InputEvents", "Input Events");  // can rename as appropriate
    man->CreateNtupleIColumn("fEvent"); //I/D correspond to integer/double
    man->CreateNtupleDColumn("fX_in");
    man->CreateNtupleDColumn("fY_in");
    man->CreateNtupleDColumn("fPx_in");
    man->CreateNtupleDColumn("fPy_in");
    man->CreateNtupleDColumn("fPz_in");
    man->CreateNtupleDColumn("fTheta_in");
    man->CreateNtupleDColumn("fPhi_in");
    man->CreateNtupleDColumn("fP_in");
    man->CreateNtupleDColumn("fP_T_in");
    man->FinishNtuple();

    // Create Ntuple for Output Events (no decay)
    man->CreateNtuple("OutputEvents", "Output Events");  // can rename as appropriate
    man->CreateNtupleIColumn("fEvent"); //I/D correspond to integer/double
    man->CreateNtupleDColumn("fX_out");
    man->CreateNtupleDColumn("fY_out");
    man->CreateNtupleDColumn("fPx_out");
    man->CreateNtupleDColumn("fPy_out");
    man->CreateNtupleDColumn("fPz_out");
    man->CreateNtupleDColumn("fTheta_out");
    man->CreateNtupleDColumn("fPhi_out");
    man->CreateNtupleDColumn("fP_out");
    man->CreateNtupleDColumn("fP_T_out");
    man->FinishNtuple();

    // Create Ntuple for All Events (including decay events)
    man->CreateNtuple("AllEvents", "All Events");
    man->CreateNtupleIColumn("fEvent");
    man->CreateNtupleIColumn("fIsDecayed");
    man->CreateNtupleIColumn("fIsTransmitted");
    man->FinishNtuple();

    man->CreateH2("Position_in","Pos_in",101, -50, 50, 101, -50, 50);
    man->CreateH2("Position_out","Pos_out",101, -50, 50, 101, -50, 50);
    man->CreateH2("P_in_vs_P_out", "P_in_vs_P_out", 201, 20, 50, 201, 20, 50);
    man->CreateH2("Theta_in_vs_Theta_out", "Theta_in_vs_Theta_out",91,150,180,91,150,180);
}

void RunAction::EndOfRunAction(const G4Run*) {
    // ========== Write and Close .root file ==========
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->Write();
    man->CloseFile();
}