from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double
from sys import exit
import os
import argparse

#Create parser
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-root-file', type=str, required=True, help='Inpot ROOT file', dest='inputFile')
#parser.add_argument('-o','--output-root-file', type=str, required=True, help='Output ROOT file', dest='onputFile')
args = parser.parse_args()
print 'Arguments provided :',args

#Open input file
rootFile = TFile(args.inputFile, 'READ')
if (rootFile.IsOpen == False): 
  print "ERROR: ROOT file",args.inputFile,"opening failed"
  exit(-1)

#Get directories
UTriggersV = rootFile.Get('UTriggersV')
if not UTriggersV : 
  print "Error getting UTriggersV"
  exit(-1)

#
# Doublet drift time pairs
#

#Get hist
g_doubletDriftTimes = UTriggersV.Get('g_doubletDriftTimes')
if not g_doubletDriftTimes : 
  print "Error getting g_doubletDriftTimes"
  exit(-1)

#Fit it
linfit = TF1("linfit", "[0] + [1]*x", 0, 50)
linfit.SetParameters(10, -1)
g_doubletDriftTimes.Fit("linfit")
intercept = linfit.GetParameter(0)
slope = linfit.GetParameter(1)

#Draw it
g_doubletDriftTimes.SetTitle('Drift times in V layer doublet straw pairs (t0 from U layer doublet)')
#g_doubletDriftTimes.SetStats(False)
g_doubletDriftTimes.GetXaxis().SetTitle('Drift time (straw 0) [ns]')
g_doubletDriftTimes.GetYaxis().SetTitle('Drift time (straw 1) [ns]')
g_doubletDriftTimes.GetYaxis().SetTitleOffset(1.2)
g_doubletDriftTimes.GetXaxis().SetRangeUser(-10.,60.)
g_doubletDriftTimes.GetYaxis().SetRangeUser(-10.,60.)
g_doubletDriftTimes.SetMarkerStyle(7)
g_doubletDriftTimes.Draw("AP")
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
for i in range(0, g_doubletDriftTimes.GetN() ) :

  #Calculate residual
  driftTime0 = Double(0)
  driftTime1 = Double(0)
  g_doubletDriftTimes.GetPoint(i,driftTime0,driftTime1)
  residual = driftTime1 - ( slope*driftTime0 + intercept );
          
  #Fill histo
  h_residuals.Fill(residual)

#Draw it
h_residuals.Draw()
raw_input("Press Enter to continue...")

