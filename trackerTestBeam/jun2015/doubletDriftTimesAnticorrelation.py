from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double
from sys import exit
import os
import argparse
import RootHelper as rh

#Create parser
#parser = argparse.ArgumentParser(description='')
#args = parser.parse_args()
#print 'Arguments provided :',args

#Inputs
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/run00404/deadTime150ns/mtestDriftTimesFromOtherView.root'
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/run00404/deadTime150ns/mtestRecoAnalysis_siliconTriggersStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/sim/idealCase_testSiT0/mtestRecoAnalysis_siliconTriggersStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/sim/strawEff40/MO-60-30-8-2/mtestRecoAnalysis_siliconTriggersStraws.root'
#rootDirName = 'UTriggersV'
rootDirName = 'SiliconTriggersStraws/StrawDoublets/'
graphName = 'g_doubletDriftTimes' 

#Open input file
rootFile = rh.openFile(rootFileName)

#
# Doublet drift time pairs
#

#Get drift time pair graph
gr = rh.getFromFile(rootFile,rootDirName+graphName)

#Fit it
linfit = TF1("linfit", "[0] + [1]*x", -10., 60.)
linfit.SetParameters(50., -1)
gr.Fit("linfit","R") #R enforces range of TF1 for fit
intercept = linfit.GetParameter(0)
slope = linfit.GetParameter(1)

#Draw it
gr.SetTitle('Drift times in V layer doublet straw pairs (t0 from U layer doublet)')
#gr.SetStats(False)
gr.GetYaxis().SetTitleOffset(1.2)
gr.GetXaxis().SetRangeUser(-10.,60.)
gr.GetYaxis().SetRangeUser(-10.,60.)
gr.SetMarkerStyle(7)
gr.Draw("AP")
raw_input("Press Enter to continue...")


#
# Doublet drift time residuals
#

#Book histo
h_residuals = TH1F('h_residuals','Drift time residuals to fit [ns]', 100, -50., 50.)
h_residuals.GetXaxis().SetTitle('Drift time residual to fit [ns]')
h_residuals.GetYaxis().SetTitle('Counts')
h_residuals.GetYaxis().SetTitleOffset(1.2)

#Get residuals for all points on graph and fill histo
for i in range(0, gr.GetN() ) :

  #Calculate residual
  driftTime0 = Double(0)
  driftTime1 = Double(0)
  gr.GetPoint(i,driftTime0,driftTime1)
  residual = driftTime1 - ( slope*driftTime0 + intercept );
          
  #Fill histo
  h_residuals.Fill(residual)

#Draw it
h_residuals.Draw()
raw_input("Press Enter to continue...")

