#include "DetectorConstruction.hh"

DetectorConstruction::DetectorConstruction(G4int config, G4double thickness) {
    fConfig = config;
    fPlateThickness = thickness;
}

DetectorConstruction::~DetectorConstruction() {

}

G4VPhysicalVolume *DetectorConstruction::Construct() {
    // ========== Define Materials ==========
    G4NistManager *nist = G4NistManager::Instance();
    G4Material *plateMaterial = nullptr;

    // Vacuum
    G4double atomicNumber = 1.;
    G4double massOfMole = 1.008*g/mole;
    G4double density = 1.e-25*g/cm3;
    G4double temperature = 2.73*kelvin;
    G4double pressure = 3.e-18*pascal;
    G4Material *Vacuum = new G4Material("vacuum", atomicNumber, massOfMole, density, kStateGas, temperature, pressure);

    // Gold
    G4Material *gold = nist->FindOrBuildMaterial("G4_Au");


    switch (fConfig) {
        // Copper (Elemental)
        case 0: {
            G4Material *copper = nist->FindOrBuildMaterial("G4_Cu");
            plateMaterial = copper;
            break;
        }
    
        // Glass (75% SiO2, 12% CaO, 13% Na2O)
        case 1: {
            G4Element *Na = new G4Element("Sodium", "Na", 11., 22.990*g/mole);
            G4Element *O = new G4Element("Oxygen"  , "O", 8. , 16.00*g/mole);
            G4Element *Ca = new G4Element("Calcium", "Ca", 20., 40.078*g/mole);
            G4Element *Si = new G4Element("Silicon","Si",14., 28.0855*g/mole);

            G4String SiO2name = "SiO2";
            const std::vector<G4String> SiO2elm {"Si", "O"};
            const std::vector<G4int> SiO2nbAtoms {1,2};
            G4Material* SiO2 = nist->ConstructNewMaterial(SiO2name, SiO2elm, SiO2nbAtoms, 2.65*g/(cm*cm*cm), true, kStateSolid, CLHEP::STP_Temperature, CLHEP::STP_Pressure);

            G4String CaOname = "CaO";
            const std::vector<G4String> CaOelm {"Ca", "O"};
            const std::vector<G4int> CaOnbAtoms {1,1};
            G4Material* CaO = nist->ConstructNewMaterial(CaOname, CaOelm, CaOnbAtoms, 3.34*g/(cm*cm*cm), true, kStateSolid, CLHEP::STP_Temperature, CLHEP::STP_Pressure);

            G4String Na2Oname = "Na2O";
            const std::vector<G4String> Na2Oelm {"Na", "O"};
            const std::vector<G4int> Na2OnbAtoms {2,1};
            G4Material* Na2O = nist->ConstructNewMaterial(Na2Oname, Na2Oelm, Na2OnbAtoms, 2.27*g/(cm*cm*cm), true, kStateSolid, CLHEP::STP_Temperature, CLHEP::STP_Pressure);

            G4Material *Glass = new G4Material("Glass", density=2.68*g/(cm*cm*cm), 3);
            Glass->AddMaterial(SiO2,75*perCent);
            Glass->AddMaterial(CaO,12*perCent);
            Glass->AddMaterial(Na2O,13*perCent);

            plateMaterial = Glass;

            break;
        }

        // Copper (Elemental)
        case 2: {
            G4Material *copper = nist->FindOrBuildMaterial("G4_Cu");
            plateMaterial = copper;
            break;
        }

        // Default (Copper)
        default: {
            G4Material *copper = nist->FindOrBuildMaterial("G4_Cu");
            plateMaterial = copper;
            break;
        }
    }

    G4double coatingThickness = 5*um;

    // ========== Construct Shapes ==========
    // World
    G4Box *solidWorld = new G4Box("solidWorld", 1*m, 1*m, 1*m); //Lengths are half lengths (0.5->1), standard distance (mm)
    G4LogicalVolume *logicWorld = new G4LogicalVolume(solidWorld, Vacuum, "logicWorld");
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0, G4ThreeVector(0.,0.,0.), logicWorld, "physWorld", 0, false, 0, true); // rotation, center pos, logic volume, name, inside other volume?, boolean operations, copy number, should check for overlaps?
    G4VisAttributes *worldVisAttributes = new G4VisAttributes(0);

    // Scattering Plate
    G4Box *solidPlate = new G4Box("solidPlate", 1*m, fPlateThickness*mm, 1*m);
    G4LogicalVolume *logicPlate = new G4LogicalVolume(solidPlate, plateMaterial, "logicPlate");
    G4VPhysicalVolume *physPlate = new G4PVPlacement(0, G4ThreeVector(0., -1*(fPlateThickness*mm), 0.), logicPlate, "physPlate", logicWorld, false, 0, true); // rotation, center pos, logic volume, name, inside other volume?, boolean operations, copy number, should check for overlaps?

    G4Box *solidCoatingGold = nullptr;
    G4LogicalVolume *logicCoatingGold = nullptr;
    G4VPhysicalVolume *physCoatingGold = nullptr;
    if (fConfig == 2) {
        solidCoatingGold = new G4Box("solidCoatingGold", 1*m, coatingThickness, 1*m);
        logicCoatingGold = new G4LogicalVolume(solidCoatingGold, gold, "logicalCoatingGold");
        physCoatingGold = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicCoatingGold, "physCoatingGold", logicWorld, false, 0, true);
    }



    // ========== Set Visualization Attributes ==========
    
    G4VisAttributes* plateVisAttributes = new G4VisAttributes();
    G4VisAttributes* coatingVisAttributes = new G4VisAttributes();
    switch (fConfig) {
        case 0:
            plateVisAttributes->SetColour(G4Colour::Brown());
            break;
        case 1:
            plateVisAttributes->SetColour(G4Colour::Gray());
            break;
        case 2:
            plateVisAttributes->SetColour(G4Colour::Brown());
            coatingVisAttributes->SetColour(G4Colour::Yellow());
            coatingVisAttributes->SetForceSolid(true);
            logicCoatingGold->SetVisAttributes(coatingVisAttributes);
            break;
        default:
            plateVisAttributes->SetColour(G4Colour::White());
            break;

    }
    plateVisAttributes->SetForceSolid(true);  // Enable solid visualization
    logicPlate->SetVisAttributes(plateVisAttributes);

    // ========== Set Step Size in Volumes ===========
    G4double maxStep = 0.1*mm;
    G4UserLimits *stepLimit = new G4UserLimits(maxStep);
    logicPlate->SetUserLimits(stepLimit);
    if (fConfig == 2) {
        logicCoatingGold->SetUserLimits(stepLimit);
    }

    // ========== Return World ==========
    return physWorld;
}