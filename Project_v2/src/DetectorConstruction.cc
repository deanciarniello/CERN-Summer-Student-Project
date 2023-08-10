/*
File: DetectorConstruction.cc
Author: Dean Ciarniello
Date: 2023-08-09
*/

// Includes
// ===================================================
#include "DetectorConstruction.hh"

// DetectorConstruction Constructor
// Info: Extracts capillary configuration parameters from capillaryConfig
// ===================================================
DetectorConstruction::DetectorConstruction(G4int capillaryMaterial, G4int capillaryShape, std::vector<G4double> capillaryConfig) {
    fCapillaryMaterial = capillaryMaterial;
    fCapillaryShape = capillaryShape;
    fCapillaryConfig = capillaryConfig;

    switch (fCapillaryShape) {
        case 0: {
            fPolyOrder = fCapillaryConfig.at(0);
            fStartRadius = fCapillaryConfig.at(1)*mm;
            fEndRadius = fCapillaryConfig.at(2)*mm;
            fLength = fCapillaryConfig.at(3)*mm;
            fThickness = fCapillaryConfig.at(4)*mm;
            fZ = fCapillaryConfig.at(5);
            break;
        }

        case 1: {
            fStartRadius = fCapillaryConfig.at(0)*mm;
            fEndRadius = fCapillaryConfig.at(1)*mm;
            fLength = fCapillaryConfig.at(2)*mm;
            fThickness = fCapillaryConfig.at(3)*mm;
            fZ = fCapillaryConfig.at(4);
            break;
        }
    }
}

// DetectorConstruction Destructor
// ===================================================
DetectorConstruction::~DetectorConstruction() {

}

// DetectorConstruction Construct
// Info: Constructs the geometry and detectors for the simulation
// ===================================================
G4VPhysicalVolume *DetectorConstruction::Construct() {
    // ========== Define Materials ==========
    G4NistManager *nist = G4NistManager::Instance();
    G4Material *capillaryMaterial = nullptr;

    // ===== Vacuum =====
    G4double atomicNumber = 1.;
    G4double massOfMole = 1.008*g/mole;
    G4double density = 1.e-25*g/cm3;
    G4double temperature = 2.73*kelvin;
    G4double pressure = 3.e-18*pascal;
    G4Material *Vacuum = new G4Material("vacuum", atomicNumber, massOfMole, density, kStateGas, temperature, pressure);

    // ===== Gold =====
    G4Material *gold = nist->FindOrBuildMaterial("G4_Au");

    // Depeding on the detector configuration, set the capillary material to the corresponding material
    switch (fCapillaryMaterial) {
        // Copper (Elemental)
        case 0: {
            G4Material *copper = nist->FindOrBuildMaterial("G4_Cu");
            capillaryMaterial = copper;
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

            capillaryMaterial = Glass;

            break;
        }

        // Copper (Elemental) with gold plating
        case 2: {
            G4Material *copper = nist->FindOrBuildMaterial("G4_Cu");
            capillaryMaterial = copper;
            break;
        }

        // Default (Copper)
        default: {
            G4Material *copper = nist->FindOrBuildMaterial("G4_Cu");
            capillaryMaterial = copper;
            break;
        }
    }


    // ========== Construct World ==========
    // ===== World =====
    G4Box *solidWorld = new G4Box("solidWorld", 5*m, 5*m, 5*m); //Lengths are half lengths (0.5->1), standard distance (mm)
    G4LogicalVolume *logicWorld = new G4LogicalVolume(solidWorld, Vacuum, "logicWorld");
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0, G4ThreeVector(0.,0.,0.), logicWorld, "physWorld", 0, false, 0, true); // rotation, center pos, logic volume, name, inside other volume?, boolean operations, copy number, should check for overlaps?
    G4VisAttributes *worldVisAttributes = new G4VisAttributes(0);

    // ========== Construct Capillary ==========
    // Coating thickness for gold coating option
    G4double CoatingThickness = 5*um;

    // z-planes (slices of the tessalated polycone)
    std::vector<G4double> capillary_z;
    for (int i=0; i < fZ; i++) {
        capillary_z.push_back((fLength/(fZ - 1))*i);
    }

    // radii
    std::vector<G4double> r_min;
    std::vector<G4double> r_max;
    std::vector<G4double> r_plate;

    // Compute the inner and outer for the tessalated solid
    switch (fCapillaryShape) {
        case 0: // Parabola
            r_min = this->Polynomial(capillary_z, 0);
            if (fCapillaryMaterial == 2) {
                r_plate = this->Polynomial(capillary_z, CoatingThickness);
            }
            r_max = this->Polynomial(capillary_z, fThickness);
            break;

        case 1: // Hyperbola
            r_min = this->Hyperbola(capillary_z, 0);
            if (fCapillaryMaterial == 2) {
                r_plate = this->Hyperbola(capillary_z, CoatingThickness);
            }
            r_max = this->Hyperbola(capillary_z, fThickness);
            break;
    }

    // Convert from vector to array
    G4double* r_min_a = &r_min[0];
    G4double* r_max_a = &r_max[0];
    G4double* r_plate_a = &r_plate[0];
    G4double* capillary_z_a = &capillary_z[0];

    // Initialize Volumes
    G4Polycone *solidCapillary = nullptr;
    G4LogicalVolume *logicalCapillary = nullptr;
    G4VPhysicalVolume *physCapillary = nullptr;

    G4Polycone *solidCapillaryCoating = nullptr;
    G4LogicalVolume *logicalCapillaryCoating = nullptr;
    G4VPhysicalVolume *physCapillaryCoating = nullptr;

    // Construct with correct material/coating
    switch (fCapillaryMaterial) {
        case 0: // Copper
            solidCapillary = new G4Polycone("solidCapillary", 0, 2*M_PI, fZ, capillary_z_a, r_min_a, r_max_a);
            logicalCapillary = new G4LogicalVolume(solidCapillary, capillaryMaterial, "logicalCapillary");
            physCapillary = new G4PVPlacement(0, G4ThreeVector(0.,0., -fLength), logicalCapillary, "physCapillary", logicWorld, false, 0, true);
            break;
        
        case 1: // Glass
            solidCapillary = new G4Polycone("solidCapillary", 0, 2*M_PI, fZ, capillary_z_a, r_min_a, r_max_a);
            logicalCapillary = new G4LogicalVolume(solidCapillary, capillaryMaterial, "logicalCapillary");
            physCapillary = new G4PVPlacement(0, G4ThreeVector(0.,0., -fLength), logicalCapillary, "physCapillary", logicWorld, false, 0, true);
            break;

        case 2:  // Gold Plated Copper
            solidCapillary = new G4Polycone("solidCapillary", 0, 2*M_PI, fZ, capillary_z_a, r_plate_a, r_max_a);
            logicalCapillary = new G4LogicalVolume(solidCapillary, capillaryMaterial, "logicalCapillary");
            physCapillary = new G4PVPlacement(0, G4ThreeVector(0.,0., -fLength), logicalCapillary, "physCapillary", logicWorld, false, 0, true);

            solidCapillaryCoating = new G4Polycone("solidCapillaryCoating", 0, 2*M_PI, fZ, capillary_z_a, r_min_a, r_plate_a);
            logicalCapillaryCoating = new G4LogicalVolume(solidCapillaryCoating, gold, "logicalCapillaryCoating");
            physCapillaryCoating = new G4PVPlacement(0, G4ThreeVector(0.,0., -fLength), logicalCapillaryCoating, "physCapillaryCoating", logicWorld, false, 0, true);
            break;
    }


    // ========== Construct end cap/detectors (no interaction with particles; simply for detection purposes) ==========
    G4Tubs *solidStartCap = new G4Tubs("solidStartCap",  0, fStartRadius, 1*mm, 0., 2*M_PI);
    G4Tubs *solidEndCap = new G4Tubs("solidStartCap", 0, fEndRadius, 1*mm, 0., 2*M_PI);

    G4LogicalVolume *logicalStartCap = new G4LogicalVolume(solidStartCap, Vacuum, "logicalStartCap");
    G4LogicalVolume *logicalEndCap = new G4LogicalVolume(solidEndCap, Vacuum, "logicalEndCap");
    
    G4VPhysicalVolume *physStartCap = new G4PVPlacement(0, G4ThreeVector(0.,0.,-1.*mm), logicalStartCap, "physStartCap", logicWorld, false, 0, true);
    G4VPhysicalVolume *physEndCap = new G4PVPlacement(0, G4ThreeVector(0.,0., -fLength), logicalEndCap, "physEndCap", logicWorld, false, 0, true);



    // ========== Set Visualization Attributes ==========
    G4VisAttributes* capillaryVisAttributes = new G4VisAttributes();
    G4VisAttributes* coatingVisAttributes = new G4VisAttributes();

    // Depending on the capillary configuration, assign the correct vis attributes and color
    switch (fCapillaryMaterial) {
        case 0:
            capillaryVisAttributes->SetColour(G4Colour::Brown());
            break;
        case 1:
            capillaryVisAttributes->SetColour(G4Colour::Gray());
            break;
        case 2:
            capillaryVisAttributes->SetColour(G4Colour::Brown());
            coatingVisAttributes->SetColour(G4Colour::Yellow());
            break;
        default:
            capillaryVisAttributes->SetColour(G4Colour::White());
            break;
    }
    capillaryVisAttributes->SetForceSolid(true);  // Enable solid visualization
    logicalCapillary->SetVisAttributes(capillaryVisAttributes);

    // Do the same for the gold plating option
    if (fCapillaryMaterial == 2) {
        coatingVisAttributes->SetForceSolid(true);
        logicalCapillaryCoating->SetVisAttributes(coatingVisAttributes);
    }
    
    // ========== Set Step Size in Volumes ===========
    G4double maxStep = 0.1*mm;
    G4UserLimits *stepLimit = new G4UserLimits(maxStep);
    logicalCapillary->SetUserLimits(stepLimit);
    if (fCapillaryMaterial == 2) {
        logicalCapillaryCoating->SetUserLimits(stepLimit);
    }

    // ========== Return World ==========
    return physWorld;
}



// ========== Define Mathematical Functions ==========
// Info: these functions return the values of the functions
//        at each point in the domain, and returns as a vector

// Polynomial
std::vector<G4double> DetectorConstruction::Polynomial(std::vector<G4double> domain, G4double offset) {
    std::vector<G4double> range;
    for (int i=0; i < fZ; i++) {
        range.push_back(fEndRadius + (fStartRadius - fEndRadius)*pow((1/fLength), fPolyOrder)*pow(domain.at(i), fPolyOrder) + offset);
    }
    return range;
}

// Hyperbola
std::vector<G4double> DetectorConstruction::Hyperbola(std::vector<G4double> domain, G4double offset) {
    std::vector<G4double> range;
    for (int i=0; i < fZ; i++) {
        range.push_back(fEndRadius*sqrt(1 + (pow((fStartRadius/fEndRadius),2)-1)*pow((domain.at(i))/(fLength),2)) + offset);
    }
    return range;
}