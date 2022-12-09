// Author: Daniel Bonifacio
// usage: root -b -l -q './GenerateSpectrum.C++()' > ./output/ionsource/GenerateSpectrum.txt&
// usage: root -b -l -q './GenerateSpectrum.C++()' > ./output/Mono511keV/GenerateSpectrum.txt&


#include "TTree.h"
#include "TFile.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
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

void GenerateSpectrum()
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

 Int_t nHits, eventID;
 Double_t charge;
 //TFile *fin1 = new TFile(Form("./output/ionsource/PhToCharge.root"));
 TFile *fin1 = new TFile(Form("./output/Mono511keV/PhToCharge.root"));
 cout << "Opening file output" << endl;
 if (fin1->IsZombie()) 
 {
  cout << "Unable to open file .root" << endl;
  return;
 }
 TTree *OptData = (TTree*)gDirectory->Get("Singles");
 OptData->SetBranchAddress("counts",&nHits);
 OptData->SetBranchAddress("charge",&charge);
 OptData->SetBranchAddress("eventID",&eventID);
 Int_t nEntries = OptData->GetEntries("charge>500");
 cout<<" number of entries chosen = "<< nEntries << endl;

 TCanvas* Canvas1 = new TCanvas("Canvas1","Canvas1",0,0,800,600);
 gStyle->SetPalette(1,0);
 gStyle->SetErrorX(0);
 TGaxis::SetMaxDigits(3);
 OptData->Draw("charge>>hcharge(100)", "charge>500","", nEntries,0);
 OptData->SetLineWidth(2.);
 OptData->SetTitle("");
 TH1F *hcharge = (TH1F*)gDirectory->Get("hcharge");
 hcharge->SetMarkerStyle(21);
 hcharge->SetMarkerSize(1);
 hcharge->SetTitle("");
 hcharge->GetYaxis()->SetTitle("counts");
 hcharge->GetXaxis()->SetTitle("charge");

 Int_t bin1, bin2;
 bin2 = hcharge->FindLastBinAbove(hcharge->GetMaximum()/2);
 Int_t binMax = hcharge->GetMaximumBin();
 bin1 = binMax - (bin2-binMax)-1;
cout<<" bin1 = "<< bin1 << endl;
cout<<" bin2 = "<< bin2 << endl;

 TF1 *fcharge = new TF1("fcharge", "gaus", hcharge->GetBinCenter(bin1-1), hcharge->GetBinCenter(bin2+1));
 hcharge->Fit("fcharge", "RNQ");
 Double_t meanene = fcharge->GetParameter(1);
 Double_t errmeanene = fcharge->GetParError(1);
 Double_t sigene = fcharge->GetParameter(2);
 Double_t errsigene = fcharge->GetParError(2);
 cout<<" *****Results from our simulated data**** "<< endl;
 cout<<" Mean charge = "<< meanene << "(" << errmeanene << ")" << endl;
 cout<<" FWHM charge = "<< 2.355*sigene << "(" << 2.355*errsigene << ")" << endl;
 cout<<" Charge resolution= "<< 100*2.355*sigene/meanene << "(" << 100*2.355*errsigene/meanene << ")%" << endl;
 fcharge->Draw("same");

 TLegend *leg = new TLegend(0.75,0.75,0.9,0.8);
 leg->SetFillColor(0);
 leg->SetBorderSize(1);
 leg->SetTextSize(0.04);
 leg->AddEntry(hcharge,"Na-22","lpf");
 leg->Draw("same");
 Canvas1->Update();
 //Canvas1->Print(Form("./output/ionsource/chargePT.pdf"));
 Canvas1->Print(Form("./output/Mono511keV/chargePT.pdf"));
}
