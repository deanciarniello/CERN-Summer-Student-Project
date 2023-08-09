/*
File: RunAction.cc
Author: Dean Ciarniello
Date: 2023-07-22
*/

// Includes
// ===================================================
#include "RunAction.hh"

// RunAction Constructor
// Info: set run variables
// ===================================================
RunAction::RunAction(G4String output, G4String outputPath) {
    fOutputFile = output;
    fOutputPath = outputPath;
}

// RunAction Destructor
// ===================================================
RunAction::~RunAction() {

}

// RunAction BeginOfRunAction
// Info: use analysis manager to create ntuples and histograms
// ===================================================
void RunAction::BeginOfRunAction(const G4Run*) {
    // =========== Create Ntuples and Histograms in .root file ==========
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->OpenFile(fOutputPath+fOutputFile);

    // Create Ntuple for Primary Events (no decay)
    man->CreateNtuple("PrimaryEvents", "Primary Events");  // can rename as appropriate
    man->CreateNtupleIColumn("fEvent"); //I/D correspond to integer/double
    man->CreateNtupleDColumn("fP_x");
    man->CreateNtupleDColumn("fP_y");
    man->CreateNtupleDColumn("fP_z");
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
    //man->CreateH2("Pz_vs_Theta", "Pz versus Theta", 2.5, 0., 100., 5, 0., 180.);
}

// RunAction EndOfRunAction
// Info: write to and close output .root file
// ===================================================
void RunAction::EndOfRunAction(const G4Run*) {
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->Write();
    man->CloseFile();
}