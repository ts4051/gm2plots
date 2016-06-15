#Compare mean cluster E across multiple runs

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./meanEnergyPlots.root", help='Input ROOT file containing plots from MeanElectronE module', dest='inputFile')
args = parser.parse_args()

#Open input file
rootFile = rh.openFile(args.inputFile)
if not rootFile : sys.exit(-1)

clusterRootDirName = "mean_electron_energy/cluster"

gStyle.SetOptStat(0)

mg = TMultiGraph()


#
# Get electron and laser E sum graphs
#

mg = TMultiGraph()

g_electronMeanE = rh.getFromFile(rootFile,clusterRootDirName+'/g_electronMeanE')
g_electronMeanE.SetMarkerStyle(8)
g_electronMeanE.SetMarkerSize(1)
g_electronMeanE.SetMarkerColor(kRed)
g_electronMeanE.SetLineColor(kRed)
mg.Add(g_electronMeanE)

g_laserMeanE = rh.getFromFile(rootFile,clusterRootDirName+'/g_laserMeanE')
g_laserMeanE.SetMarkerStyle(8)
g_laserMeanE.SetMarkerColor(kBlue)
g_laserMeanE.SetLineColor(kBlue)
mg.Add(g_laserMeanE)


#
# Correct e- E sum based on laser 
#

g_correctedElectronMeanE = TGraph(g_electronMeanE.GetN())

#Step through runs and make corrections
for i_point in range(0,g_electronMeanE.GetN()) :

  runNum = Double(0)
  electronMeanE = Double(0)
  g_electronMeanE.GetPoint(i_point,runNum,electronMeanE)

  laserMeanE = Double(0)
  g_laserMeanE.GetPoint(i_point,runNum,laserMeanE) #Same run num

  #Handle laser baseline calivration changes at certain runs
  laserBaseLineE = 0.
  if runNum >= 2894 and runNum <= 3048 : laserBaseLineE = 80725. #TODO
  elif runNum >= 3049 and runNum <= 9999 : laserBaseLineE = 10. #TODO
  else:
    print "No known calibration for run %i" % (runNum)
    sys.exit(-1)

  #Determine laser gain correction relative to baseline for this run
  laserCorrection = float(laserMeanE) / float(laserBaseLineE) #TODO div 0 protection

  #Correct electron E by this factor
  correctedElectronMeanE =  electronMeanE / laserCorrection
  g_correctedElectronMeanE.SetPoint(i_point,runNum,correctedElectronMeanE)


#Add corrected electron E sum to plot
g_correctedElectronMeanE.SetMarkerStyle(8)
g_correctedElectronMeanE.SetMarkerColor(kGreen)
g_correctedElectronMeanE.SetLineColor(kGreen)
mg.Add(g_correctedElectronMeanE)


#
# Calculate corrected E sum mean
#

#TODO Calculate different mean when we change calibration

#Get mean over time of corrected cluster mean E
sumMeanClusterE = 0.
numRunsUsedForSum = 0
for i_point in range(0,g_correctedElectronMeanE.GetN()) :

  runNum = Double(0)
  meanE = Double(0)
  g_correctedElectronMeanE.GetPoint(i_point,runNum,meanE)

  #Some runs are near edge of calo and E is not contained. Exclude these for mean.
  if runNum <= 2970 or runNum >= 2977 :    #Avoid step off edge
    sumMeanClusterE += meanE
    numRunsUsedForSum += 1

meanMeanClusterE = sumMeanClusterE / float(numRunsUsedForSum) if numRunsUsedForSum > 0 else 0.

#Draw mean
g_meanLine = TGraph(2)
g_meanLine.SetPoint(0,g_electronMeanE.GetXaxis().GetXmin(),meanMeanClusterE)
g_meanLine.SetPoint(1,g_electronMeanE.GetXaxis().GetXmax(),meanMeanClusterE)
mg.Add(g_meanLine)

#Draw 5% either side of mean
g_meanLinePlus5Percent = TGraph(2)
g_meanLinePlus5Percent.SetPoint(0,g_electronMeanE.GetXaxis().GetXmin(),meanMeanClusterE*1.05)
g_meanLinePlus5Percent.SetPoint(1,g_electronMeanE.GetXaxis().GetXmax(),meanMeanClusterE*1.05)
g_meanLinePlus5Percent.SetLineStyle(9)
mg.Add(g_meanLinePlus5Percent)

g_meanLineMinus5Percent = TGraph(2)
g_meanLineMinus5Percent.SetPoint(0,g_electronMeanE.GetXaxis().GetXmin(),meanMeanClusterE*0.95)
g_meanLineMinus5Percent.SetPoint(1,g_electronMeanE.GetXaxis().GetXmax(),meanMeanClusterE*0.95)
g_meanLineMinus5Percent.SetLineStyle(9)
mg.Add(g_meanLineMinus5Percent)


#
# Draw the final multigraph
#

mg.Draw("APL") #Draw once to populate axes
mg.GetXaxis().SetTitle( "Run number" )
mg.GetYaxis().SetTitle( "Mean cluster energy [photoelectrons]" )
mg.GetYaxis().SetTitleOffset(1.2)
mg.GetYaxis().SetTitleOffset(1.5)
mg.SetTitle( "Mean cluster energy per run" )
mg.Draw("APL")
raw_input("Press Enter to continue...")


