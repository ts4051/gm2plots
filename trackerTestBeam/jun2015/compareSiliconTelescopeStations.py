from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double, TCut
from sys import exit
import os
import argparse
import RootHelper as rh
import math

#Inputs
rootFileName = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00344/mtestRecoAnalysis_reconstructedSiTrackPlots.root'

#Open input file
rootFile = rh.openFile(rootFileName)


#
# Compare first and last stations
#

#Get drift time pair graph
gr = rh.getFromFile(rootFile,'Station_0/g_YvsY_Station_3')

#Fit it
fit = TF1("fit", "[0] + [1]*x", -10.e3, 10.e3)
fit.SetParameters(0., 1.)
#fit.FixParameter(1,fit.GetParameter(1)) #Fix gradient
gr.Fit("fit","R") #R enforces range of TF1 for fit
fitIntercept = fit.GetParameter(0)
fitSlope = fit.GetParameter(1)

#Draw it
#gr.GetXaxis().SetRangeUser(-10.,60.)
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
h_residuals = TH1F('h_residuals',';Residuals to fit [ns];', 1000, -2000., 2000.)

#Get residuals for all points on graph and fill histo
for i in range(0, gr.GetN() ) :

  #Calculate residual
  xAxisPoint = Double(0)
  yAxisPoint = Double(0)
  gr.GetPoint(i,xAxisPoint,yAxisPoint)
  h_residuals.Fill( residual(fitSlope,fitIntercept,xAxisPoint,yAxisPoint) )

#Fit core
h_residuals.Fit("gaus","","")

#Draw it
h_residuals.Draw()
raw_input("Press Enter to continue...")

