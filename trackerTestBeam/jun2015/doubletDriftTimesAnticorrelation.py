from ROOT import TFile, TTree, gROOT, TH1F, TCanvas, gStyle, TF1, TProfile, TH2F, TGraph, TF1, Double, TCut
from sys import exit
import os
import argparse
import RootHelper as rh
import math

#Create parser
#parser = argparse.ArgumentParser(description='')
#args = parser.parse_args()
#print 'Arguments provided :',args

#Inputs
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc/'
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc-Res_140um/'
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/singleOcc-Res_200um/'
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5/'
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Eff_80/'
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Res_140um/'
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Res_200um/'
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Eff_80-Res_200um/'
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00316/'
rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00402/'
#rootFileDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/run00404/'

#Plots
#rootFileName = 'mtestRecoAnalysis_compareSiliconTrackToStraws.root'  #If using silicon for t0
rootFileName = 'mtestDriftTimesFromOtherView.root'  #If using one straw view to trigger the other
rootFilePath = rootFileDir + "/" + rootFileName
#graphName = 'CompareTrackToStraws/StrawDoublets/g_doubletDriftTimes'   #If using silicon for t0
graphName = 'UTriggersV/g_doubletDriftTimes'   #If using one straw view to trigger the other

#Open input file
rootFile = rh.openFile(rootFilePath)


'''
#
# Doublet drift time pairs profile
#

#Get drift time pair graph
profile = rh.getFromFile(rootFile,rootDirName+"p_doubletDriftTimesCut")

#Fit it
profileFit = TF1("profileFit", "[0] + [1]*x", 15., 35.)
profileFit.SetParameters(50., -1)
profileFit.FixParameter(1,profileFit.GetParameter(1)) #Fix gradient
profile.Fit("profileFit","R") #R enforces range of TF1 for fit
profileIntercept = profileFit.GetParameter(0)
profileSlope = profileFit.GetParameter(1)

#Draw it
profile.GetXaxis().SetRangeUser(-10.,60.)
profile.Draw()
raw_input("Press Enter to continue...")
'''

#
# Doublet drift time pairs
#

#Get drift time pair graph
gr = rh.getFromFile(rootFile,graphName)

#Draw it
gr.SetTitle('Ar-Ethane 1800V 200mV')
#gr.SetStats(False)
gr.GetYaxis().SetTitleOffset(1.2)
gr.GetXaxis().SetRangeUser(-10.,60.)
gr.GetYaxis().SetRangeUser(-10.,60.)
#gr.SetMarkerStyle(7)
gr.GetXaxis().SetTitle("Drift time in straw (layer 0) [ns]")
gr.GetYaxis().SetTitle("Drift time in straw (layer 1) [ns]")
gr.Draw("AP")
raw_input("Press Enter to continue...")

#Fit it
linFit = TF1("linFit", "[0] + [1]*x", 20., 40.)
linFit.SetParameters(50., -1.05)
linFit.FixParameter(1,linFit.GetParameter(1)) #Fix gradient
gr.Fit("linFit","R") #R enforces range of TF1 for fit
intercept = linFit.GetParameter(0)
slope = linFit.GetParameter(1)

#Draw it with fit
gr.GetYaxis().SetTitle("Drift time in straw (layer 1) [ns]")
gr.Draw("AP")
#linFit.Draw("same")
raw_input("Press Enter to continue...")


#
# Doublet drift time sum
#

#Book histo
h_driftTimeSum = TH1F('h_driftTimeSum','', int(100/2.5), 0., 100.)
h_driftTimeSum.GetXaxis().SetTitle('Doublet drift time sum [ns]')
h_driftTimeSum.GetYaxis().SetTitle('Counts')
h_driftTimeSum.GetYaxis().SetTitleOffset(1.2)

#Get residuals for all points on graph and fill histo
for i in range(0, gr.GetN() ) :

  #Calculate residual
  driftTime0 = Double(0)
  driftTime1 = Double(0)
  gr.GetPoint(i,driftTime0,driftTime1)
  driftTimeSum = driftTime0 + driftTime1
  h_driftTimeSum.Fill(driftTimeSum)

#Fit
#h_residuals.Fit("gaus","","",-100.,100.)
f_driftTimeSum = TF1("f_driftTimeSum", "gaus", -0., 100.);
h_driftTimeSum.Fit("f_driftTimeSum")
f_driftTimeSumMean = f_driftTimeSum.GetParameter(1)
f_driftTimeSumSigma = f_driftTimeSum.GetParameter(2)

#Draw it
h_driftTimeSum.SetTitle('Ar-Ethane 1800V 200mV')
gStyle.SetOptStat(0)
h_driftTimeSum.Draw()
print "Drift time sum: Gaussian fit mean = %f ns, sigma = %f ns" % (f_driftTimeSumMean,f_driftTimeSumSigma)
print "Single straw sigma = %f ns" % (f_driftTimeSumSigma/math.sqrt(2.))
raw_input("Press Enter to continue...")


'''
#
# Doublet drift time pairs (cut applied to drift time sum)
#

#Get drift time pair graph
grCut = rh.getFromFile(rootFile,rootDirName+cutGraphName)
'''
'''
#Fit it
linFitCut = TF1("linFitCut", "[0] + [1]*x", 10., 40.)
linFitCut.SetParameters(50., -1)
grCut.Fit("linFitCut","R") #R enforces range of TF1 for fit
interceptCut = linFitCut.GetParameter(0)
slopeCut = linFitCut.GetParameter(1)
'''

'''
#Draw it
grCut.SetTitle('Drift times in V layer doublet straw pairs (t0 from U layer doublet) after cut')
grCut.GetYaxis().SetTitleOffset(1.2)
grCut.SetMarkerStyle(7)
grCut.GetXaxis().SetTitle("Drift time in straw (layer 0) [ns]")
grCut.GetYaxis().SetTitle("Drift time in straw (layer 1) [ns]")
grCut.Draw("AP")
profileFit.Draw("same")
raw_input("Press Enter to continue...")
'''

'''
#
# Doublet drift time pairs (uncut, but with fit to cut plot)
#

grUncutFitCut = rh.getFromFile(rootFile,graphName)
grUncutFitCut.GetYaxis().SetTitleOffset(1.2)
grUncutFitCut.GetXaxis().SetRangeUser(-50.,100.)
grUncutFitCut.GetYaxis().SetRangeUser(-50.,100.)
gr.SetMarkerStyle(7)
grUncutFitCut.Draw("AP")
linFitCut.Draw("same")
raw_input("Press Enter to continue...")
'''

#
# Doublet drift time residuals
#

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



#Book histo
h_residuals = TH1F('h_residuals','', int(200/2.5), -100., 100.)
h_residuals.GetXaxis().SetTitle('Residual to fit [ns]')
h_residuals.GetYaxis().SetTitle('Counts')
h_residuals.GetYaxis().SetTitleOffset(1.2)

#Get residuals for all points on graph and fill histo
for i in range(0, gr.GetN() ) :

  #Calculate residual
  driftTime0 = Double(0)
  driftTime1 = Double(0)
  gr.GetPoint(i,driftTime0,driftTime1)
  xRes,yRes,perpRes = residual(slope,intercept,driftTime0,driftTime1)
  h_residuals.Fill(perpRes)

#Fit core
#h_residuals.Fit("gaus","","",-100.,100.)
f_residuals = TF1("f_residuals", "gaus", -500., 500.);
h_residuals.Fit("f_residuals")
f_residualsMean = f_residuals.GetParameter(1)
f_residualsSigma = f_residuals.GetParameter(2)

#Draw it
h_residuals.SetTitle('Ar-Ethane 1800V 200mV')
gStyle.SetOptStat(0)
h_residuals.Draw()
print "Anti-correlation residuals : Gaussian fit mean = %f ns, sigma = %f ns" % (f_residualsMean,f_residualsSigma)
raw_input("Press Enter to continue...")


'''
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
  h_residualsUncutCutFit.Fill( residual(profileSlope,profileIntercept,driftTime0,driftTime1) )

#Draw it
h_residualsUncutCutFit.Draw()
raw_input("Press Enter to continue...")
'''

'''
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
  h_residualsCut.Fill( residual(profileSlope,profileIntercept,driftTime0,driftTime1) )

#Fit core
h_residualsCut.Fit("gaus","","",-100.,100.)

#Draw it
h_residualsCut.Draw()
raw_input("Press Enter to continue...")
'''
