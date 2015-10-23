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
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00402/mtestRecoAnalysis_compareSiliconTrackToStraws.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00404/mtestRecoAnalysis_compareSiliconTrackToStraws.root'

#Open input file
rootFile = rh.openFile(rootFileName)


#
# Compare first and last stations
#

#Get drift time pair graph
gr = rh.getFromFile(rootFile,'CompareTrackToStraws/StrawDoublets/g_trackToWireDCA_vs_driftTime')

#Draw it
gr.SetTitle("Ar-Ethane 1800V 200mV")
gr.GetXaxis().SetTitle("Track DCA to straw [mm]")
gr.GetYaxis().SetTitle("Straw drift time [ns]")
gr.GetXaxis().SetRangeUser(0.,2.5)
gr.GetYaxis().SetRangeUser(0.,100.)
gr.SetMarkerStyle(7)
gr.Draw("AP")
raw_input("Press Enter to continue...")

#Fit it
fit = TF1("fit", "[0] + [1]*x", 1., 2.)
fit.SetParameters(0., 20.8) #Initial guesses
#fit.FixParameter(0,fit.GetParameter(0)) #Fix intercept
fit.FixParameter(1,fit.GetParameter(1)) #Fix gradient
#fit.SetParLimits(1, 0.99, 1.01) #Limit gradient
gr.Fit("fit","R") #R enforces range of TF1 for fit
fitIntercept = fit.GetParameter(0)
fitSlope = fit.GetParameter(1)
driftVelocity = 1.e3 / fitSlope
print "Drift velocity =",driftVelocity,"[um/ns]"

#Draw it again with fit
gr.Draw("AP")
raw_input("Press Enter to continue...")



#
# Get residuals
#

#Function to get residuals
def residual(m,c,x,y) :

  #Convert from y=mx+c to more general ax+by+c=0 => a=m,b=-1
  a = m
  b = -1

  #Calculate DCA
  dca = abs( a*x + b*y + c ) / math.sqrt( math.pow(a,2) + math.pow(b,2) )

  #Get sign (+ve means above fit line)
  sign = 1. if y > m*x+c else -1.

  res = sign * dca
  return res


#Book histo
h_residuals = TH1F('h_residuals',';Residuals to fit;', 120, -3.e3, 3.e3)

#Get residuals for all points on graph and fill histo
for i in range(0, gr.GetN() ) :

  #Calculate residual
  xAxisPoint = Double(0)
  yAxisPoint = Double(0)
  gr.GetPoint(i,xAxisPoint,yAxisPoint)
  h_residuals.Fill( residual(fitSlope,fitIntercept,xAxisPoint*1.e3,yAxisPoint*1.e3) )

#Fit core
#h_residuals.Fit("gaus","","")
f_residuals = TF1("f_residuals", "gaus", -1.5e3, 1.5e3);
h_residuals.Fit("f_residuals","R")

#Draw it
h_residuals.Draw()
raw_input("Press Enter to continue...")

