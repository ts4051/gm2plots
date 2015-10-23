from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double, TCut
from sys import exit
import os
import argparse
import RootHelper as rh
import math

#Inputs
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc-Res_140um/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc-Res_200um/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Eff_80/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Res_140um/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Res_200um/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Eff_80-Res_200um/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00402/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00404/mtestRecoAnalysis_compareSiliconTrackToStraws.root'

#Open input file
rootFile = rh.openFile(rootFileName)



#
# Look at uncertainty in detector offsets
#

gStyle.SetOptStat(0)

glibClockPeriodNs = 25.

#Loop over straw views
views = ["U","V"]
for view in views :

  print view,"view:"

  #Get time offset plot
  h_detectorOffset = rh.getFromFile(rootFile,'CompareTrackToStraws/TimeSync/'+view+'/h_detectorOffset')

  #Have offsets around n*25ns where n=0,-1,-2,-3. Fit Guassian to each
  nVals = [0,-1,-2,-3]
  for n in nVals :

    expectedOffset = float(n) * glibClockPeriodNs

    #Perform fit
    window = 0.5 * glibClockPeriodNs
    fitName = "f_detectorOffset_%s_n%s" % ( view, str(n) )
    f_detectorOffset = TF1(fitName,"gaus", expectedOffset-window, expectedOffset+window)
    h_detectorOffset.Fit(fitName,"R") #R enforces range of TF1 for fit
    mean = f_detectorOffset.GetParameter(1)
    sigma = f_detectorOffset.GetParameter(2)
    print "%s view : n = %i : Mean = %f ns : sigma = %f ns " % (view,n,mean,sigma)

  #Draw hist and fits
  h_detectorOffset.Draw("AP")
  raw_input("Press Enter to continue...")


