# GateSiPM

The modeling of the ionizing radiation detector plays an important role in optimizing its performance, since it allows understanding the parameters that influence the electronic signal formation. This framework simulates the photon counting spectrum and the charge/electronic signal (pulse or waveform) produced by a detector composed of a scintillating material (e.g. LYSO) coupled to a silicon photomultiplier (SiPM).

Macro script files were implemented in GATE (http://www.opengatecollaboration.org/) version 9.2 to simulate ionizing radiation interaction with the scintillation material. Scintillation photons are collected by the SiPM (defined as a GATE sensitive detector) and the hits data is stored in a ROOT (https://root.cern/) format file. The ROOT code converts optical photons one by one directly from GATE hits data into signal waveforms and integrated charge events using open source C++ classes from GosSiP:

Macro script files were implemented in GATE (http://www.opengatecollaboration.org/) version 9.2 to simulate the interaction of ionizing radiation with the scintillation material. The scintillation photons are collected by the SiPM (defined as a GATE-sensitive detector) and the hits data are stored in a file in ROOT format (https://root.cern/). ROOT code converts one-by-one optical photons into signal waveforms and charge events using GosSiP's open source C++ classes:

http://dx.doi.org/10.1088/1748-0221/7/08/P08011

The original GosSiP code can be obtained from:
https://bitbucket.org/kip-hep-detectors/gossip/src/master/

Be aware that this approach is very realistic despite being computationally intensive.

#1. GATE SIMULATION

The GATE scripts are located in the "mac" folder. In the "python" folder, there is a script called "generateOpticalSinglePixelmac.py" that helps to define the crystal and SiPM dimensions for the GATE simulation. You just need to edit the user section of the script and then run:

python generateOpticalSinglePixelmac.py

The generated mac files should be moved from the "python" to the "mac" folder.

As an example, you can run a single stand-alone simulation using:

Gate -a [WrappingMaterial,PTFE][CrystalMaterial,LYSO-Ce-Hilger][LateralSurface,PTFE_wrapped][TopSurface,PTFE_wrapped][X,0][Y,0][i,0][j,0] mac/mainMacroionsource.mac > output/ionsource/term_output00.txt&

This setup comprises as primary particle the unstable radionuclide (i.e. monatomic ion source) sodium-22 that decays by emitting beta + (positron) particles with a branching fraction of 0.90. Some of the isotropically emitted annihilation photons will interact within the scintillation crystal (3 x 3 x 10 mm3) and the deposited energy will be partially converted into optical photons. All relevant optical processes are simulated and some of these optical photons will be detected by a perfect photosensor (i.e. photon detection efficiency is 1). Energy, time, position and identification of each photon hit are recorded in a ROOT file at the "output/ionsource" folder. The selected parameters define a LYSO crystal wrapped by a PTFE tape to improve scintillation light collection. The ion source is centered at the XY plane of the crystal. The main macro "mainMacroionsource.mac" calls the other macros for a complete simulation. The parameters options are:

WrappingMaterial: PTFE or Epoxy

CrystalMaterial: LYSO-Ce-Hilger, LYSO-Proteus or LFS-3

LateralSurface and TopSurface: PTFE_wrapped, Air, smooth or BlackEpoxyPaint

X and Y coordinates represent the source position with respect to the entrance surface of the crystal (XY plane).

i and j are the id for the incident position in the root file output

There is also another example called "mainMacroMono.mac", which uses directional 511 keV photons as primary particles. For further study, the user can use a shell script to perform simulations with different parameters. For instance, see the bash scripts run.sh file and its editable parameters:

"offsetx" and "offsety" define, in mm, the offsets distance from the crystal center (0,0) of the gamma incidence in the XY plane

"npointsx" and "npointsy" define the number of scanning points in X and Y directions;

"sizex" and "sizex" define crystal size in the XY plane

"nsimproc" controls the number of running Gate simulations at the same time.

To execute it, run:

chmod +x run.sh

And then:

./run.sh

#2. OPTICAL PHOTONS TO CHARGE CONVERSION USING ROOT CODE

The following ROOT script converts optical hits data from GATE output file (in ROOT format) into charge events using GosSiP classes:

root -b -l -q './PhotonCountingToChargeByPixelID.C++("./PhotonToCharge.cfg")' > ./output/rootoutput.txt&

You can generate a charge spectrum using the command:

root -b -l -q './GenerateSpectrum.C++()' > ./output/ionsource/GenerateSpectrum.txt&

Notice that the code lines for waveform generation are commented, because it is (more) computing intensive. The waveform is represented using the TGraph ROOT class.
