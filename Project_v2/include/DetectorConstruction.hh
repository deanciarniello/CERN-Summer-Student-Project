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
#include "G4CSGSolid.hh"
#include "G4Cons.hh"
#include "G4Hype.hh"
#include "G4VCSGfaceted.hh"
#include "G4Polycone.hh"
#include "G4Tubs.hh"
#include "G4SubtractionSolid.hh"

#include <cmath>

class DetectorConstruction : public G4VUserDetectorConstruction 
{
public:
    DetectorConstruction(G4int capillaryMaterial, G4int capillaryShape, std::vector<G4double> capillaryConfig);
    ~DetectorConstruction();

    virtual G4VPhysicalVolume *Construct();

    std::vector<G4double> Polynomial(std::vector<G4double> domain, G4double offset);
    std::vector<G4double> Hyperbola(std::vector<G4double> domain, G4double offset);

    G4double fStartRadius;
    G4double fEndRadius;
    G4double fLength;
    G4int fPolyOrder;
    G4double fThickness;
    G4int fZ;

private:
    G4int fCapillaryMaterial;
    G4int fCapillaryShape;
    std::vector<G4double> fCapillaryConfig;
};


#endif