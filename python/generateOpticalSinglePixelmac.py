# generateCylindricalPETmac.py
# Python script to generate a GATE macro to describe a PET scanner based on monolithic crystal

## User section
##Parameters to be edited by the user
## The unit of length is always mm

#SiPM array dimensions
SiPMPixSizeX = 6.07
SiPMPixSizeY = 6.07
SiPMPitchSizeX = 7.00
SiPMPitchSizeY = 7.00
nSiPMX = 1
nSiPMY = 1
#monolithic crystal dimensions
CSizeX = SiPMPitchSizeX*nSiPMX-(SiPMPitchSizeX-SiPMPixSizeX)
CSizeY = SiPMPitchSizeY*nSiPMY-(SiPMPitchSizeY-SiPMPixSizeY)
CSizeZ = 6.00 #crystal thickness
#module array
NModX = 1 #number of rings
ModPitchSizeX = CSizeX + 4.80
NModY = 1
ModPitchSizeY = CSizeY + 4.80
#ring or rsector
NrsectorPerRing = 1 #number of heads per ring
#optical grease thickness
OptCouplingThick = 0.01
#Top crystal layer (opposite to the SiPM array)
TopCrystalThick = 1.00
#silicon thickness
SiThick = 0.10
# SiPM epoxy cover
SiPMCoverThick = 0.4
# Module Cover Thickness
ModCoverThick = 2.00
##Do not edit the parameters beyond this line!!!
##End of the user section

##GATE parameters section
##Do not edit the following parameters!!!

#OpticalSystem
XOpticalSystem = ModPitchSizeX + 20.00
YOpticalSystem = ModPitchSizeY + 20.00
ZOpticalSystem = CSizeZ + 2*ModCoverThick
#module
Xmodule = NModX*ModPitchSizeX
Ymodule = NModY*ModPitchSizeY
Zmodule = CSizeZ + 2*ModCoverThick
#monolithic crystal dimensions
Xcrystal = CSizeX
Ycrystal = CSizeY
Zcrystal = CSizeZ
#optical coupling
Xoptcoup = CSizeX
Yoptcoup = CSizeY
Zoptcoup = OptCouplingThick
TranslationZoptcoup = CSizeZ/2+Zoptcoup/2
#Top crystal layer (opposite to the SiPM array)
Xtopcrys = CSizeX
Ytopcrys = CSizeY
Ztopcrys = TopCrystalThick
TranslationZtopcrys = -CSizeZ/2-Ztopcrys/2
# SiPM epoxy cover
XSiPMCover = SiPMPixSizeX
YSiPMCover = SiPMPixSizeY
ZSiPMCover = SiPMCoverThick
TranslationZSiPMCover = CSizeZ/2 + ZSiPMCover/2 + Zoptcoup
# SiPM array
XSiPM = SiPMPixSizeX
YSiPM = SiPMPixSizeY
ZSiPM = SiThick
TranslationZSiPM = CSizeZ/2 + ZSiPM/2 + ZSiPMCover + Zoptcoup

f = open('SinglePixelpy.mac','w')
f.write('# This macro describes a PET monolithic crystal detector block')
f.write('\n' + '# the block consists of a ' + str(CSizeX) + ' x ' + str(CSizeY) + ' x ' + str(CSizeZ) + ' mm3 crystal coupled to a SiPM array')
f.write('\n' + '# of ' + str(nSiPMX) + ' x ' + str(nSiPMY) + ' elements with '  + str(SiPMPixSizeX) + ' x ' + str(SiPMPixSizeY) + ' mm2 each one.' )
f.write('\n')
f.write('\n' + '#### Using Optical system ####')
f.write('\n' + '/gate/world/daughters/name OpticalSystem')
f.write('\n' + '/gate/world/daughters/insert box')
f.write('\n' + '/gate/OpticalSystem/setMaterial Air')
f.write('\n' + '/gate/OpticalSystem/geometry/setXLength ' + str(XOpticalSystem) + ' mm')
f.write('\n' + '/gate/OpticalSystem/geometry/setYLength ' + str(YOpticalSystem) + ' mm')
f.write('\n' + '/gate/OpticalSystem/geometry/setZLength ' + str(ZOpticalSystem) + ' mm')
f.write('\n' + '/gate/OpticalSystem/vis/forceWireframe 1')
f.write('\n')
f.write('\n' + '/gate/OpticalSystem/daughters/name module')
f.write('\n' + '/gate/OpticalSystem/daughters/insert box')
f.write('\n' + '/gate/module/geometry/setXLength ' + str(Xmodule) + ' mm')
f.write('\n' + '/gate/module/geometry/setYLength ' + str(Ymodule) + ' mm')
f.write('\n' + '/gate/module/geometry/setZLength ' + str(Zmodule) + ' mm')
f.write('\n' + '/gate/module/setMaterial {WrappingMaterial}')
f.write('\n' + '/gate/module/vis/forceWireframe')
f.write('\n')
f.write('\n' + '/gate/module/daughters/name crystal')
f.write('\n' + '/gate/module/daughters/insert box')
f.write('\n' + '/gate/crystal/geometry/setXLength ' + str(Xcrystal) + ' mm')
f.write('\n' + '/gate/crystal/geometry/setYLength ' + str(Ycrystal) + ' mm')
f.write('\n' + '/gate/crystal/geometry/setZLength ' + str(Zcrystal) + ' mm')
f.write('\n' + '/gate/crystal/setMaterial {CrystalMaterial}')
f.write('\n' + '/gate/crystal/placement/setTranslation    0. 0. 0. mm')
f.write('\n' + '/gate/crystal/vis/setColor yellow')
f.write('\n')
# === Top crystal layer (opposite to the SiPM array) ===
f.write('\n' + '/gate/module/daughters/name TopCrystalLayer')
f.write('\n' + '/gate/module/daughters/insert box')
f.write('\n' + '/gate/TopCrystalLayer/geometry/setXLength ' + str(Xtopcrys) + ' mm')
f.write('\n' + '/gate/TopCrystalLayer/geometry/setYLength ' + str(Ytopcrys) + ' mm')
f.write('\n' + '/gate/TopCrystalLayer/geometry/setZLength ' + str(Ztopcrys) + ' mm')
f.write('\n' + '/gate/TopCrystalLayer/setMaterial {WrappingMaterial}')
f.write('\n' + '/gate/TopCrystalLayer/vis/setColor yellow')
f.write('\n' + '/gate/TopCrystalLayer/placement/setTranslation 0. 0. ' + str(TranslationZtopcrys) + ' mm')
f.write('\n')
# === Optical coupling ===
f.write('\n' + '/gate/module/daughters/name OpticalCoupling')
f.write('\n' + '/gate/module/daughters/insert box')
f.write('\n' + '/gate/OpticalCoupling/geometry/setXLength ' + str(Xoptcoup) + ' mm')
f.write('\n' + '/gate/OpticalCoupling/geometry/setYLength ' + str(Yoptcoup) + ' mm')
f.write('\n' + '/gate/OpticalCoupling/geometry/setZLength ' + str(Zoptcoup) + ' mm')
f.write('\n' + '/gate/OpticalCoupling/setMaterial VisiloxV-788')
f.write('\n' + '/gate/OpticalCoupling/vis/setColor yellow')
f.write('\n' + '/gate/OpticalCoupling/placement/setTranslation 0. 0. ' + str(TranslationZoptcoup) + ' mm')
f.write('\n')
# === SiPM cover window ===
f.write('\n' + '/gate/module/daughters/name SiPMCover')
f.write('\n' + '/gate/module/daughters/insert box')
f.write('\n' + '/gate/SiPMCover/geometry/setXLength ' + str(XSiPMCover) + ' mm')
f.write('\n' + '/gate/SiPMCover/geometry/setYLength ' + str(YSiPMCover) + ' mm')
f.write('\n' + '/gate/SiPMCover/geometry/setZLength ' + str(ZSiPMCover) + ' mm')
f.write('\n' + '/gate/SiPMCover/setMaterial Quartz')
f.write('\n' + '/gate/SiPMCover/vis/setColor blue')
f.write('\n' + '/gate/SiPMCover/placement/setTranslation 0. 0. ' + str(TranslationZSiPMCover) + ' mm')
f.write('\n' + '/gate/SiPMCover/repeaters/insert              cubicArray')
f.write('\n' + '/gate/SiPMCover/cubicArray/setRepeatNumberX ' + str(nSiPMX))
f.write('\n' + '/gate/SiPMCover/cubicArray/setRepeatNumberY ' + str(nSiPMY))
f.write('\n' + '/gate/SiPMCover/cubicArray/setRepeatNumberZ 1')
f.write('\n' + '/gate/SiPMCover/cubicArray/setRepeatVector ' + str(SiPMPitchSizeX) + ' ' + str(SiPMPitchSizeY) + ' 0. mm')
f.write('\n')
# === SiPM ===
f.write('\n' + '/gate/module/daughters/name             SiPM')
f.write('\n' + '/gate/module/daughters/insert           box')
f.write('\n' + '/gate/SiPM/geometry/setXLength ' + str(XSiPM) + ' mm')
f.write('\n' + '/gate/SiPM/geometry/setYLength ' + str(YSiPM) + ' mm')
f.write('\n' + '/gate/SiPM/geometry/setZLength ' + str(ZSiPM) + ' mm')
f.write('\n' + '/gate/SiPM/setMaterial                   Silicon')
f.write('\n' + '/gate/SiPM/vis/setColor                  red')
f.write('\n' + '/gate/SiPM/placement/setTranslation 0. 0. ' + str(TranslationZSiPM) + ' mm')
f.write('\n' + '/gate/SiPM/repeaters/insert              cubicArray')
f.write('\n' + '/gate/SiPM/cubicArray/setRepeatNumberX ' + str(nSiPMX))
f.write('\n' + '/gate/SiPM/cubicArray/setRepeatNumberY ' + str(nSiPMY))
f.write('\n' + '/gate/SiPM/cubicArray/setRepeatNumberZ  1')
f.write('\n' + '/gate/SiPM/cubicArray/setRepeatVector ' + str(SiPMPitchSizeX) + ' ' + str(SiPMPitchSizeY) + ' 0. mm')
f.write('\n')
f.write('\n' + '/gate/module/repeaters/insert cubicArray')
f.write('\n' + '/gate/module/cubicArray/setRepeatNumberX ' + str(NModX))
f.write('\n' + '/gate/module/cubicArray/setRepeatNumberY ' + str(NModY))
f.write('\n' + '/gate/module/cubicArray/setRepeatNumberZ 1')
f.write('\n' + '/gate/module/cubicArray/setRepeatVector ' + str(ModPitchSizeX) + ' ' + str(ModPitchSizeY) + ' 0. mm')
f.write('\n')
f.write('\n' + '/gate/systems/OpticalSystem/pixel/attach SiPMCover')
f.write('\n' + '/gate/systems/OpticalSystem/crystal/attach crystal')
f.write('\n')
f.write('\n' + '/gate/crystal/attachCrystalSD')
f.write('\n' + '/gate/SiPMCover/attachCrystalSD')
f.write('\n')
f.close()

f = open('opticalsurfacespy.mac','w')
f.write('\n' + '# === surfaces ===')
f.write('\n' + '/gate/crystal/surfaces/name              crystal_module')
f.write('\n' + '/gate/crystal/surfaces/insert            module')
f.write('\n' + '#CrystalSurface (BlackEpoxyPaint, PTFE_wrapped,  Air or smooth)')
f.write('\n' + '/gate/crystal/surfaces/crystal_module/setSurface {LateralSurface}')
f.write('\n')
f.write('\n' + '/gate/crystal/surfaces/name              crystal_topcrystallayer')
f.write('\n' + '/gate/crystal/surfaces/insert            TopCrystalLayer')
f.write('\n' + '#CrystalSurface (BlackEpoxyPaint, PTFE_wrapped,  Air or smooth)')
f.write('\n' + '/gate/crystal/surfaces/crystal_topcrystallayer/setSurface {TopSurface}')
f.write('\n')
f.write('\n' + '/gate/crystal/surfaces/name              optcoupsurf')
f.write('\n' + '/gate/crystal/surfaces/insert            OpticalCoupling')
f.write('\n' + '/gate/crystal/surfaces/optcoupsurf/setSurface smooth')
f.write('\n')
f.write('\n' + '/gate/OpticalCoupling/surfaces/name              crystalbacksurf')
f.write('\n' + '/gate/OpticalCoupling/surfaces/insert            crystal')
f.write('\n' + '/gate/OpticalCoupling/surfaces/crystalbacksurf/setSurface smooth')
f.write('\n')
f.write('\n' + '/gate/OpticalCoupling/surfaces/name              SiPMCoversurf')
f.write('\n' + '/gate/OpticalCoupling/surfaces/insert            SiPMCover')
f.write('\n' + '/gate/OpticalCoupling/surfaces/SiPMCoversurf/setSurface smooth')
f.write('\n')
f.write('\n' + '/gate/OpticalCoupling/surfaces/name              lateralsurf')
f.write('\n' + '/gate/OpticalCoupling/surfaces/insert            module')
f.write('\n' + '/gate/OpticalCoupling/surfaces/lateralsurf/setSurface smooth')
f.write('\n')
f.write('\n' + '/gate/SiPMCover/surfaces/name              SiPMCoverbacksurf')
f.write('\n' + '/gate/SiPMCover/surfaces/insert            OpticalCoupling')
f.write('\n' + '/gate/SiPMCover/surfaces/SiPMCoverbacksurf/setSurface smooth')
f.write('\n')
f.write('\n' + '/gate/SiPMCover/surfaces/name              lateralsurf')
f.write('\n' + '/gate/SiPMCover/surfaces/insert            module')
f.write('\n' + '/gate/SiPMCover/surfaces/lateralsurf/setSurface smooth')
f.write('\n')
f.write('\n' + '/gate/SiPMCover/surfaces/name              SiPMsurf')
f.write('\n' + '/gate/SiPMCover/surfaces/insert            SiPM')
f.write('\n' + '/gate/SiPMCover/surfaces/SiPMsurf/setSurface perfect_apd')
f.write('\n')

f.close()

