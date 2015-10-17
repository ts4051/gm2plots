from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double, TCut, kBlue
from sys import exit
import os
import argparse
import RootHelper as rh
import math

#Inputs
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc/mtestRecoAnalysis_compareSiliconTrackToStrawModuleRecoHit.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5/mtestRecoAnalysis_compareSiliconTrackToStrawModuleRecoHit.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Eff_80/mtestRecoAnalysis_compareSiliconTrackToStrawModuleRecoHit.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc-Res_200um/mtestRecoAnalysis_compareSiliconTrackToStrawModuleRecoHit.root'
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00402/mtestRecoAnalysis_compareSiliconTrackToStrawModuleRecoHit.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00404/mtestRecoAnalysis_compareSiliconTrackToStrawModuleRecoHit.root'

#Open input file
rootFile = rh.openFile(rootFileName)


#
# Fit y residuals
#

#Get histo
h_yResiduals = rh.getFromFile(rootFile,'CompareTrackToStrawModuleRecoHit/h_recoHitToTrackYResidual')

#Fit core
f_yResiduals = TF1("f_yResiduals", "gaus", -500., 500.);
h_yResiduals.Fit("f_yResiduals","R")

#Draw it
h_yResiduals.GetXaxis().SetRangeUser(-750.,750.) #[um]
h_yResiduals.Draw()

#Draw expected distribution
f_yResidualsExpected = TF1("f_yResidualsExpected", "gaus", -500., 500.);
f_yResidualsExpected.SetParameters(10.,0.,100.) #Norm,mean,sigma
f_yResidualsExpected.SetLineColor(kBlue);
f_yResidualsExpected.Draw("same")

raw_input("Press Enter to continue...")



#
# Fit z residuals
#

#Get histo
h_zResiduals = rh.getFromFile(rootFile,'CompareTrackToStrawModuleRecoHit/h_recoHitToTrackZResidual')

#Fit core
f_zResiduals = TF1("f_zResiduals", "gaus", -2000., 2000.);
h_zResiduals.Fit("f_zResiduals","R")

#Draw it
h_zResiduals.GetXaxis().SetRangeUser(-3000.,3000.) #[um]
h_zResiduals.Draw()

#Draw expected distribution
f_zResidualsExpected = TF1("f_zResidualsExpected", "gaus", -3000.,3000.);
f_zResidualsExpected.SetParameters(8.,0.,750.) #Norm,mean,sigma
f_zResidualsExpected.SetLineColor(kBlue);
f_zResidualsExpected.Draw("same")

raw_input("Press Enter to continue...")


