from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double, TCut
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
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/run00402/deadTime150ns/tmp/mtestRecoAnalysis_siliconTriggersStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/sim/idealCase_testSiT0/mtestRecoAnalysis_siliconTriggersStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/sim/strawEff40/MO-60-30-8-2/mtestRecoAnalysis_siliconTriggersStraws.root'
#rootDirName = 'UTriggersV'
rootDirName = 'SiliconTriggersStraws/StrawDoublets/'
#rootDirName = 'SiliconTriggersStraws/StrawSeeds/'
graphName = 'g_doubletDriftTimes' 
cutGraphName = 'g_doubletDriftTimesCut' 

#Open input file
rootFile = rh.openFile(rootFileName)

#
# Doublet drift time pairs
#

#Get drift time pair graph
gr = rh.getFromFile(rootFile,rootDirName+graphName)

#Fit it
linFit = TF1("linFit", "[0] + [1]*x", -10., 60.)
linFit.SetParameters(50., -1)
gr.Fit("linFit","R") #R enforces range of TF1 for fit
intercept = linFit.GetParameter(0)
slope = linFit.GetParameter(1)

#Draw it
gr.SetTitle('Drift times in V layer doublet straw pairs (t0 from U layer doublet)')
#gr.SetStats(False)
gr.GetYaxis().SetTitleOffset(1.2)
#gr.GetXaxis().SetRangeUser(-10.,60.)
#gr.GetYaxis().SetRangeUser(-10.,60.)
gr.SetMarkerStyle(7)
gr.Draw("AP")
raw_input("Press Enter to continue...")



#
# Doublet drift time pairs (cut applied to drift time sum)
#

#Get drift time pair graph
grCut = rh.getFromFile(rootFile,rootDirName+cutGraphName)

#Fit it
linFitCut = TF1("linFitCut", "[0] + [1]*x", -10., 60.)
linFitCut.SetParameters(50., -1)
grCut.Fit("linFitCut","R") #R enforces range of TF1 for fit
interceptCut = linFitCut.GetParameter(0)
slopeCut = linFitCut.GetParameter(1)

#Draw it
grCut.SetTitle('Drift times in V layer doublet straw pairs (t0 from U layer doublet) after cut')
#gr.SetStats(False)
grCut.GetYaxis().SetTitleOffset(1.2)
#grCut.GetXaxis().SetRangeUser(-10.,60.)
#grCut.GetYaxis().SetRangeUser(-10.,60.)
grCut.SetMarkerStyle(7)
grCut.Draw("AP")
raw_input("Press Enter to continue...")



#
# Doublet drift time pairs (uncut, but with fit to cut plot)
#

grUncutFitCut = rh.getFromFile(rootFile,rootDirName+graphName)
grUncutFitCut.GetYaxis().SetTitleOffset(1.2)
grUncutFitCut.GetXaxis().SetRangeUser(-50.,100.)
grUncutFitCut.GetYaxis().SetRangeUser(-50.,100.)
gr.SetMarkerStyle(7)
grUncutFitCut.Draw("AP")
linFitCut.Draw("same")
raw_input("Press Enter to continue...")



#
# Doublet drift time residuals
#

#Book histo
h_residuals = TH1F('h_residuals','Drift time residuals to fit [ns]', int(200/2.5), -100., 100.)
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

#Fit core
h_residuals.Fit("gaus","","",-17.,20.)

#Draw it
h_residuals.Draw()
raw_input("Press Enter to continue...")


#
# Doublet drift time residuals (cut fit on uncut data points)
#

#Book histo
h_residualsUncutCutFit = TH1F('h_residualsUncutCutFit','Drift time residuals (uncut data but cut fit) [ns]', int(200/2.5), -100., 100.)
h_residualsUncutCutFit.GetXaxis().SetTitle('Drift time residual to cut fit [ns]')
h_residualsUncutCutFit.GetYaxis().SetTitle('Counts')
h_residualsUncutCutFit.GetYaxis().SetTitleOffset(1.2)

#Get residuals for all points on graph and fill histo
for i in range(0, gr.GetN() ) :

  #Calculate residual
  driftTime0 = Double(0)
  driftTime1 = Double(0)
  gr.GetPoint(i,driftTime0,driftTime1)
  residualToCutFit = driftTime1 - ( slopeCut*driftTime0 + interceptCut );
          
  #Fill histo
  h_residualsUncutCutFit.Fill(residualToCutFit)

#Draw it
h_residualsUncutCutFit.Draw()
raw_input("Press Enter to continue...")


#
# Doublet drift time residuals (cut fit on cut data points)
#

#Book histo
h_residualsCut = TH1F('h_residualsCut','Drift time residuals (cut data and fit) [ns]', int(200/2.5), -100., 100.)
h_residualsCut.GetXaxis().SetTitle('Drift time residual to cut fit [ns]')
h_residualsCut.GetYaxis().SetTitle('Counts')
h_residualsCut.GetYaxis().SetTitleOffset(1.2)

#Get residuals for all points on graph and fill histo
for i in range(0, grCut.GetN() ) :

  #Calculate residual
  driftTime0 = Double(0)
  driftTime1 = Double(0)
  grCut.GetPoint(i,driftTime0,driftTime1)
  residualToCutFit = driftTime1 - ( slopeCut*driftTime0 + interceptCut );
          
  #Fill histo
  h_residualsCut.Fill(residualToCutFit)

#Fit core
h_residualsCut.Fit("gaus","","",-17.,20.)

#Draw it
h_residualsCut.Draw()
raw_input("Press Enter to continue...")
