from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double, TCut
from sys import exit
import os
import argparse
import RootHelper as rh
import math

#Inputs
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc/mtestRecoAnalysis_compareSiliconTrackToStrawModuleRecoHit.root'
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5/mtestRecoAnalysis_compareSiliconTrackToStrawModuleRecoHit.root'

#Open input file
rootFile = rh.openFile(rootFileName)


#
# Fit DCA plot
#

#Get histo
h_dca = rh.getFromFile(rootFile,'CompareTrackToStrawModuleRecoHit/h_recoHitToTrackDCAZoom')

#Fit core
f_dca = TF1("f_dca", "gaus", 0., 200.);
h_dca.Fit("f_dca","R")

#Draw it
h_dca.GetXaxis().SetRangeUser(0.,500.) #[um]
h_dca.Draw()
raw_input("Press Enter to continue...")


#
# Fit y residuals
#

#Get histo
h_yResiduals = rh.getFromFile(rootFile,'CompareTrackToStrawModuleRecoHit/h_recoHitToTrackYResidual')

#Fit core
f_yResiduals = TF1("f_yResiduals", "gaus", -300., 300.);
h_yResiduals.Fit("f_yResiduals","R")

#Draw it
h_yResiduals.GetXaxis().SetRangeUser(-500.,500.) #[um]
h_yResiduals.Draw()
raw_input("Press Enter to continue...")



#
# Fit z residuals
#

#Get histo
h_zResiduals = rh.getFromFile(rootFile,'CompareTrackToStrawModuleRecoHit/h_recoHitToTrackZResidual')

#Fit core
f_zResiduals = TF1("f_zResiduals", "gaus", -300., 300.);
h_zResiduals.Fit("f_zResiduals","R")

#Draw it
h_zResiduals.GetXaxis().SetRangeUser(-500.,500.) #[um]
h_zResiduals.Draw()
raw_input("Press Enter to continue...")


