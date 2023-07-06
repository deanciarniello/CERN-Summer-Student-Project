#ifndef CONSTRUCTION_HH
#define CONSTRUCTION_HH

#include "G4SystemOfUnits.hh"
#include "G4VUserDetectorConstruction.hh"
#include "G4Box.hh"
#include "G4PVPlacement.hh"
#include "G4NistManager.hh"
#include "G4VPhysicalVolume.hh"
#include "G4LogicalVolume.hh"
#include "G4VisAttributes.hh"
#include "G4ProcessManager.hh"
#include "G4UserLimits.hh"
#include "G4Material.hh"

#include <cmath>

class DetectorConstruction : public G4VUserDetectorConstruction 
{
public:
    DetectorConstruction(G4int detectorConfig);
    ~DetectorConstruction();

    virtual G4VPhysicalVolume *Construct();

private:
    G4int fConfig;
};


#endif