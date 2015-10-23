from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double, TCut
from sys import exit
import os
import argparse
import RootHelper as rh
import math

#Inputs
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc/mtestRecoAnalysis_compareTrackToStrawDoublets.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc-Res_140um/mtestRecoAnalysis_compareTrackToStrawDoublets.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc-Res_200um/mtestRecoAnalysis_compareTrackToStrawDoublets.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5/mtestRecoAnalysis_compareTrackToStrawDoublets.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Eff_80/mtestRecoAnalysis_compareTrackToStrawDoublets.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Res_140um/mtestRecoAnalysis_compareTrackToStrawDoublets.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Res_200um/mtestRecoAnalysis_compareTrackToStrawDoublets.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Eff_80-Res_200um/mtestRecoAnalysis_compareTrackToStrawDoublets.root'
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00402/mtestRecoAnalysis_compareTrackToStrawDoublets.root'
#rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00404/mtestRecoAnalysis_compareTrackToStrawDoublets.root'

#Open input file
rootFile = rh.openFile(rootFileName)



#Function to get residuals
def residual(m,c,x,y) :

  #Convert from y=mx+c to more general ax+by+c=0 => a=m,b=-1
  a = m
  b = -1

  #Calculate DCA residual (e.g. perpendicular to line)
  dca = abs( a*x + b*y + c ) / math.sqrt( math.pow(a,2) + math.pow(b,2) )
  sign = 1. if y > m*x+c else -1. #Get sign (+ve means above fit line)
  perpRes = sign * dca

  #Get x residual
  xRes = x - ((y-c)/m)

  #Get y residual
  yRes = y - ((m*x)+c)

  return xRes,yRes,perpRes



#
# Compare first and last stations
#

gStyle.SetOptStat(0)

#Get drift time pair graph
gr = rh.getFromFile(rootFile,'CompareTrackToStrawDoublets/g_trackToWireDCA_vs_driftDist')

#Draw it
gr.SetTitle('Ar-Ethane 1800V 300mV')
gr.GetXaxis().SetTitle('Silicon track to straw wire DCA [mm]')
gr.GetYaxis().SetTitle('Drift distance in straw [mm]')
gr.GetXaxis().SetRangeUser(0.,3.)
gr.GetYaxis().SetRangeUser(0.,3.)
gr.SetMarkerStyle(7)
gr.Draw("AP")
raw_input("Press Enter to continue...")

#Fit it
fit = TF1("fit", "[0] + [1]*x", 1., 2.)
fit.SetParameters(0., 1.) #Initial guesses
fit.FixParameter(1,fit.GetParameter(1)) #Fix gradient
#fit.SetParLimits(1, 0.99, 1.01) #Limit gradient
gr.Fit("fit","R") #R enforces range of TF1 for fit
fitIntercept = fit.GetParameter(0)
fitSlope = fit.GetParameter(1)

#Draw it again with fit
gr.Draw("AP")
raw_input("Press Enter to continue...")


#
# Get residuals
#


#Book histo
h_residuals = TH1F('h_residuals','Ar-Ethane 1800V 300mV; y residuals to fit [um];', 120, -3.e3, 3.e3)

#Get residuals for all points on graph and fill histo
for i in range(0, gr.GetN() ) :

  #Calculate residual
  xAxisPoint = Double(0)
  yAxisPoint = Double(0)
  gr.GetPoint(i,xAxisPoint,yAxisPoint)
  xRes,yRes,perpRes = residual(fitSlope,fitIntercept,xAxisPoint*1.e3,yAxisPoint*1.e3)
  h_residuals.Fill( yRes ) #y residual is resolution

#Fit core
#h_residuals.Fit("gaus","","")
f_residuals = TF1("f_residuals", "gaus", -1.5e3, 1.5e3);
h_residuals.Fit("f_residuals","R")

#Draw it
h_residuals.Draw()
raw_input("Press Enter to continue...")


#
# Cut outliers and refit
#

#Cut outliers from graph
grCut = TGraph()
cutVal = 0.75
for i in range(0, gr.GetN() ) :
  xAxisPoint = Double(0)
  yAxisPoint = Double(0)
  gr.GetPoint(i,xAxisPoint,yAxisPoint)
  xRes,yRes,perpRes = residual(fitSlope,fitIntercept,xAxisPoint,yAxisPoint)
  if math.fabs(yRes) < cutVal :
    grCut.SetPoint( grCut.GetN() , xAxisPoint, yAxisPoint  )

#Refit
cutFit = TF1("cutFit", "[0] + [1]*x", 1., 2.)
cutFit.SetParameters(0., 1.) #Initial guesses
#cutFit.FixParameter(1,fit.GetParameter(1)) #Fix gradient
#fit.SetParLimits(1, 0.99, 1.01) #Limit gradient
grCut.Fit("cutFit","R") #R enforces range of TF1 for fit
cutFitIntercept = cutFit.GetParameter(0)
cutFitSlope = cutFit.GetParameter(1)

#Draw it
grCut.SetTitle('Ar-Ethane 1800V 300mV')
grCut.GetXaxis().SetTitle('Silicon track to straw wire DCA [mm]')
grCut.GetYaxis().SetTitle('Drift distance in straw [mm]')
grCut.GetXaxis().SetRangeUser(0.,3.)
grCut.GetYaxis().SetRangeUser(0.,3.)
grCut.Draw("AP")
raw_input("Press Enter to continue...")


#
# Get residuals to the refit
#


#Book histo
h_residualsCut = TH1F('h_residualsCut','Ar-Ethane 1800V 300mV;Residuals to fit [um];', 120, -3.e3, 3.e3)

#Get residuals for all points on graph and fill histo
for i in range(0, grCut.GetN() ) :

  #Calculate residual
  xAxisPoint = Double(0)
  yAxisPoint = Double(0)
  grCut.GetPoint(i,xAxisPoint,yAxisPoint)
  xRes,yRes,perpRes = residual(cutFitSlope,cutFitIntercept,xAxisPoint*1.e3,yAxisPoint*1.e3)
  h_residualsCut.Fill( yRes )

#Fit core
#h_residuals.Fit("gaus","","")
f_residualsCut = TF1("f_residualsCut", "gaus", -1.5e3, 1.5e3);
h_residualsCut.Fit("f_residualsCut","R")

#Draw it
h_residualsCut.Draw()
raw_input("Press Enter to continue...")

