#Compare gain correction for each crystal

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./validateGainCorrection.root", help='Input ROOT file containing plots from ValidateGainCorrection module', dest='inputFile')
args = parser.parse_args()

#Open input file
rootFile = rh.openFile(args.inputFile)
if not rootFile : sys.exit(-1)

gStyle.SetOptStat(0)



#
# Compare laser cluster E
#

clusterRootDirName = "gain_correction/clusters"

mg_laserClusters = TMultiGraph()

g_meanLaserEnergy = rh.getFromFile(rootFile,clusterRootDirName+'/g_meanLaserEnergy')
g_meanLaserEnergy.SetMarkerStyle(1)
g_meanLaserEnergy.SetMarkerSize(1)
g_meanLaserEnergy.SetMarkerColor(kRed)
g_meanLaserEnergy.SetLineColor(kRed)
mg_laserClusters.Add(g_meanLaserEnergy)

g_meanCorrectedLaserEnergy = rh.getFromFile(rootFile,clusterRootDirName+'/g_meanCorrectedLaserEnergy')
g_meanCorrectedLaserEnergy.SetMarkerStyle(1)
g_meanCorrectedLaserEnergy.SetMarkerSize(1)
g_meanCorrectedLaserEnergy.SetMarkerColor(kBlue)
g_meanCorrectedLaserEnergy.SetLineColor(kBlue)
mg_laserClusters.Add(g_meanCorrectedLaserEnergy)

mg_laserClusters.Draw("APL") #Draw once to populate axes
mg_laserClusters.GetXaxis().SetTitle( "Fill time [s]" )
mg_laserClusters.GetYaxis().SetTitle( "Laser cluster E [photoelectrons]" )
mg_laserClusters.GetYaxis().SetTitleOffset(1.2)
mg_laserClusters.GetYaxis().SetTitleOffset(1.5)
mg_laserClusters.Draw("APL")
raw_input("Press Enter to continue...")


#
# Compare e- cluster E
#

mg_electronClusters = TMultiGraph()

g_meanElectronEnergy = rh.getFromFile(rootFile,clusterRootDirName+'/g_meanElectronEnergy')
g_meanElectronEnergy.SetMarkerStyle(1)
g_meanElectronEnergy.SetMarkerSize(1)
g_meanElectronEnergy.SetMarkerColor(kRed)
g_meanElectronEnergy.SetLineColor(kRed)
mg_electronClusters.Add(g_meanElectronEnergy)

g_meanCorrectedElectronEnergy = rh.getFromFile(rootFile,clusterRootDirName+'/g_meanCorrectedElectronEnergy')
g_meanCorrectedElectronEnergy.SetMarkerStyle(1)
g_meanCorrectedElectronEnergy.SetMarkerSize(1)
g_meanCorrectedElectronEnergy.SetMarkerColor(kBlue)
g_meanCorrectedElectronEnergy.SetLineColor(kBlue)
g_meanCorrectedElectronEnergy.SetLineStyle(3)
mg_electronClusters.Add(g_meanCorrectedElectronEnergy)

mg_electronClusters.Draw("APL") #Draw once to populate axes
mg_electronClusters.GetXaxis().SetTitle( "Fill time [s]" )
mg_electronClusters.GetYaxis().SetTitle( "Electron cluster E [photoelectrons]" )
mg_electronClusters.GetYaxis().SetTitleOffset(1.2)
mg_electronClusters.GetYaxis().SetTitleOffset(1.5)
mg_electronClusters.Draw("APL")
raw_input("Press Enter to continue...")




#
# Draw cluster gain correction
#

g_clusterGainCorrection = rh.getFromFile(rootFile,clusterRootDirName+'/g_gainCorrection')
g_clusterGainCorrection.SetMarkerStyle(1)
g_clusterGainCorrection.SetMarkerSize(1)
g_clusterGainCorrection.SetMarkerColor(kRed)
g_clusterGainCorrection.SetLineColor(kRed)
g_clusterGainCorrection.GetXaxis().SetTitle( "Fill time [s]" )
g_clusterGainCorrection.GetYaxis().SetTitle( "Cluster gain correction" )
g_clusterGainCorrection.GetYaxis().SetTitleOffset(1.2)
g_clusterGainCorrection.GetYaxis().SetTitleOffset(1.5)
g_clusterGainCorrection.Draw("APL")
raw_input("Press Enter to continue...")


