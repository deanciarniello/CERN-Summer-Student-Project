#include "DetectorConstruction.hh"

DetectorConstruction::DetectorConstruction() {

}

DetectorConstruction::~DetectorConstruction() {

}

G4VPhysicalVolume *DetectorConstruction::Construct() {
    G4NistManager *nist = G4NistManager::Instance();
    //G4Material *air = nist->FindOrBuildMaterial("G4_AIR");

    G4double atomicNumber = 1.;
    G4double massOfMole = 1.008*g/mole;
    G4double density = 1.e-25*g/cm3;
    G4double temperature = 2.73*kelvin;
    G4double pressure = 3.e-18*pascal;
    G4Material *vacuum = new G4Material("interGalactic", atomicNumber, massOfMole, density, kStateGas, temperature, pressure);
    G4Material *copper = nist->FindOrBuildMaterial("G4_Cu");

    // Each shape needs 3 volumes
    G4Box *solidWorld = new G4Box("solidWorld", 1*m, 1*m, 1*m); //Lengths are half lengths (0.5->1), standard distance (mm)
    G4LogicalVolume *logicWorld = new G4LogicalVolume(solidWorld, vacuum, "logicWorld");
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0, G4ThreeVector(0.,0.,0.), logicWorld, "physWorld", 0, false, 0, true); // rotation, center pos, logic volume, name, inside other volume?, boolean operations, copy number, should check for overlaps?
    G4VisAttributes *worldVisAttributes = new G4VisAttributes(0);

    G4Box *solidPlate = new G4Box("solidPlate", 1*m, 0.5*mm, 1*m);
    G4LogicalVolume *logicPlate = new G4LogicalVolume(solidPlate, copper, "logicPlate");
    G4VPhysicalVolume *physPlate = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicPlate, "physPlate", logicWorld, false, 0, true); // rotation, center pos, logic volume, name, inside other volume?, boolean operations, copy number, should check for overlaps?

    G4VisAttributes* plateVisAttributes = new G4VisAttributes(G4Colour(0.7, 0.45, 0.2));
    //plateVisAttributes->SetVisibility(true);
    plateVisAttributes->SetForceSolid(true);  // Enable solid visualization
    logicPlate->SetVisAttributes(plateVisAttributes);

    return physWorld; //return phys volume
}