#include "construction.hh"

DetectorConstruction::DetectorConstruction() {

}

DetectorConstruction::~DetectorConstruction() {

}

G4VPhysicalVolume *DetectorConstruction::Construct() {
    G4NistManager *nist = G4NistManager::Instance();
    G4Material *air = nist->FindOrBuildMaterial("G4_AIR");
    G4Material *copper = nist->FindOrBuildMaterial("G4_Cu");

    // Each shape needs 3 volumes
    G4Box *solidWorld = new G4Box("solidWorld", 1*m, 1*m, 1*m); //Lengths are half lengths (0.5->1), standard distance (mm)
    G4LogicalVolume *logicWorld = new G4LogicalVolume(solidWorld, air, "logicWorld");
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0, G4ThreeVector(0.,0.,0.), logicWorld, "physWorld", 0, false, 0, true); // rotation, center pos, logic volume, name, inside other volume?, boolean operations, copy number, should check for overlaps?

    G4Box *solidPlate = new G4Box("solidPlate", 1*m, 0.5*mm, 1*m);
    G4LogicalVolume *logicPlate = new G4LogicalVolume(solidPlate, copper, "logicPlate");
    G4VPhysicalVolume *physPlate = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicPlate, "physPlate", logicWorld, false, 0, true); // rotation, center pos, logic volume, name, inside other volume?, boolean operations, copy number, should check for overlaps?

    G4VisAttributes* plateVisAttributes = new G4VisAttributes(G4Colour(0.7, 0.45, 0.2));  // brown??
    plateVisAttributes->SetVisibility(true);
    plateVisAttributes->SetForceSolid(true);  // Enable solid visualization
    logicPlate->SetVisAttributes(plateVisAttributes);

    return physWorld; //return phys volume
}