from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double, TCut
from sys import exit
import os
import argparse
import RootHelper as rh
import math

#Inputs
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc/mtestRecoAnalysis_compareSiliconTrackToStrawModuleRecoHit.root'

#Open input file
rootFile = rh.openFile(rootFileName)


#
# Fit DCA plot
#

#Get histo
h_dca = rh.getFromFile(rootFile,'CompareTrackToStrawModuleRecoHit/h_recoHitToTrackDCAZoom')

#Fit core
h_dca.Fit("gaus","","")

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
h_yResiduals.Fit("gaus","","")

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
h_zResiduals.Fit("gaus","","")

#Draw it
h_zResiduals.GetXaxis().SetRangeUser(-500.,500.) #[um]
h_zResiduals.Draw()
raw_input("Press Enter to continue...")


