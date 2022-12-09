// This ROOT code converts optical photons one by one directly from GATE hits data into signal waveforms and integrated charge events using open source C++ classes from GosSiP
// Author: Daniel Bonifacio
// usage: root -b -l -q './PhotonCountingToChargeByPixelID.C++("./PhotonToCharge.cfg")' > ./output/ionsource/rootoutput.txt&
// usage: root -b -l -q './PhotonCountingToChargeByPixelID.C++("./PhotonToCharge.cfg")' > ./output/Mono511keV/rootoutput.txt&

#include "TTree.h"
#include "TFile.h"
#include "TEventList.h"
#include "TEntryList.h"
#include "Riostream.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <vector>
#include <TF1.h>
#include <TH2.h>
#include <TLegend.h>
#include <TPolyMarker.h>
#include <TFile.h>
#include <TTree.h>
#include <TStyle.h>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <TCanvas.h>
#include <TGaxis.h>
#include <TProfile.h>

#include "gossip/sipmMC.cpp"
#include "gossip/PhotonList.cpp"
#include "gossip/HitMatrix.cpp"

void PhotonCountingToChargeByPixelID(const char *configfile)
{
 gStyle->SetOptStat(0);
 gStyle->SetCanvasColor(kWhite);     // background is no longer mouse-dropping white
 gStyle->SetPalette(1,0);            // blue to red false color palette. Use 9 for b/w
 gStyle->SetCanvasBorderMode(0);     // turn off canvas borders
 gStyle->SetPadBorderMode(0);
 gStyle->SetPaintTextFormat("5.2f");  // What precision to put numbers if plotted with "TEXT"
 gStyle->SetHistFillColor(kWhite);
 gStyle->SetLineWidth(2.);
 gStyle->SetTextSize(0.8);
 gStyle->SetMarkerSize(2); 
 gStyle->SetLabelSize(0.05,"xy");
 gStyle->SetTitleSize(0.05,"xy");
 gStyle->SetPadTopMargin(0.09);
 gStyle->SetPadRightMargin(0.08);
 gStyle->SetPadBottomMargin(0.12);
 gStyle->SetPadLeftMargin(0.14);
 gStyle->SetStripDecimals(kFALSE);

 string temp;
 Int_t nPOI;
 ofstream outtxtfile;
 ifstream myfile (configfile);
 cout.setf(ios::fixed);
 cout.setf(ios::left);
 cout<<setprecision(2);
 cout<<setw(8);
 cout << "Checking config file..." << endl;
 if (myfile.is_open())
 {
  cout << "Reading config file..." << endl; 
  myfile >> temp >> nPOI;
  myfile.close();
 }
 else
 {
  cout << "Unable to open config file." << endl; 
  return;
 }

    sipmMC *sipm = new sipmMC();					///create instance of sipmMC
	sipm->GetParaFile("input/MPPC_3x3.txt");		///read in sipm parameters for file MPPC_3x3.txt
	sipm->SetSampling(0.2);					///set sampling rate to 0.2ns ( = 5 GSPS )
	sipm->SetGate(500);					///set measurement window to 500 ns
	sipm->SetPreGate(200);					///set simulation time before measurement window to 500 ns

	TFile f("input/SpectralSensitivity.root");
	sipm->SetSpectralSensitivity((TGraph*)f.Get("MPPC_noRef"));
	f.Close();

//auto fout = TFile::Open("output/ionsource/PhToCharge.root","RECREATE");
auto fout = TFile::Open("output/Mono511keV/PhToCharge.root","RECREATE");
Int_t nEntries, pixelID, runID, eventID, eventIDold, eventIDProc, nHits=0, PDGEncoding;
Float_t posX, posY, posZ, edep, posXProc, posYProc, edepProc, wavelength; //pos in mm, edep in MeV and wavelength in nm
Double_t time, timeProc; //in seconds
PhotonList photons;		///Photon list to be processed by sipm simulation
double charge;			///sipm output charge
//TGraph *waveform;		///sipm output waveform
TTree Singles("Singles","Singles Tree with counts and charge variables");
Singles.Branch("counts",&nHits,"nHits/I");
Singles.Branch("charge",&charge,"charge/D");
Singles.Branch("eventID",&eventID,"eventID/I");

TFile *fin[nPOI][nPOI];
Int_t p=0,q=0;
 while (q<nPOI)
 {       
  p=0;
  while (p<nPOI)
  { 
   //fin[p][q] = new TFile(Form("./output/ionsource/output%i%i.hits.root",p,q));
   fin[p][q] = new TFile(Form("./output/Mono511keV/output%i%i.hits.root",p,q));
   //fin[p][q] = new TFile(Form("./output/output%i%i.root",p,q));
   cout << "Opening file output" << p << q << ".root" << endl;
   if (fin[p][q]->IsZombie()) 
   {
    cout << "Unable to open file ./output" << p << q << ".root" << endl;
    return;
   }
   //TTree *OptData = (TTree*)gDirectory->Get("Hits");
   TTree *OptData = (TTree*)gDirectory->Get("tree");
   OptData->SetBranchStatus("*",0);
   OptData->SetBranchStatus("edep",1);
   OptData->SetBranchStatus("time",1);
   OptData->SetBranchStatus("posX",1);
   OptData->SetBranchStatus("posY",1);
   OptData->SetBranchStatus("pixelID",1);
   OptData->SetBranchStatus("eventID",1);
   OptData->SetBranchStatus("PDGEncoding",1);
   OptData->SetBranchAddress("edep",&edep);
   OptData->SetBranchAddress("time",&time);
   OptData->SetBranchAddress("posX",&posX);
   OptData->SetBranchAddress("posY",&posY);
   OptData->SetBranchAddress("posZ",&posZ);
   OptData->SetBranchAddress("pixelID",&pixelID);
   OptData->SetBranchAddress("eventID",&eventID);
   OptData->SetBranchAddress("PDGEncoding",&PDGEncoding);

   Double_t firsttime;
   Int_t nStart, nEnd, nDetectedEvts = 0;
   Int_t nEntries = OptData->GetEntries();
   cout<<" nEntries= "<< nEntries << endl;
   for(int n=0;n<nEntries;n++)
   {
    OptData->GetEntry(n);
    firsttime=time;
    nStart=n;
    nEnd=n;
    eventIDold=eventID;
    cout<<" eventID= "<< eventID << endl;
    while ((eventIDold==eventID) && (n<nEntries))
    {
     if (PDGEncoding==-22 && pixelID==0)
     { 
      if (firsttime>time) firsttime = time; //in seconds
     }
     n++;
     OptData->GetEntry(n);
    }
    n=n-1;
    nEnd=n;
    for (int m=nStart;m<nEnd+1;m++)
    {
     OptData->GetEntry(m); 
     if (PDGEncoding==-22 && pixelID==0)
     {    
      wavelength = 1239.8/(edep*1e6);
      photons.AddPhoton(posX,posY,TMath::Abs(time-firsttime)*1e9,wavelength);///add photon to the photon list
      nHits++;
     } 
    }
    nDetectedEvts++;
    sipm->Generate(photons);			///generate sipm response from photon list
	charge = sipm->GetCharge();			///get output signal charge
    //if (charge < 0.) charge=0;
	//waveform = sipm->GetWaveform();			///get output waveform
    Singles.Fill();
    cout<<" nHits= "<< nHits << endl;
    cout<<" charge= "<< charge << endl;
    nHits = 0;
    photons.clear();
   }
   cout<<" End of scan!!! Detected Events = "<< nDetectedEvts << endl;
   fout->Write();
   p++;
  }
  q++;
 }
}
