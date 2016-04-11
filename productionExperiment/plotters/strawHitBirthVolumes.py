#Plot birth pos and hit pos for particles hitting straws from certain volumes

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./truthPlots.root", help='Input ROOT file containing plots from StrawAndCaloTruthPlots module', dest='inputFile')
args = parser.parse_args()


#Open input file
rootFile = rh.openFile(args.inputFile)

#Plotting function
def plotBirthAndHitPositionsFromChosenVolume(particle,station,volume,xRange,yRange) :

  mg = TMultiGraph()

  #Get birth points and add to multi-graph
  g_birthPos = rh.getFromFile(rootFile,'straw_calo_truth/%s/tracker/station_%i/g_birthPosTop_%s' % (particle,station,volume) )
  g_birthPos.SetMarkerColor(kGreen)
  mg.Add(g_birthPos)

  #Get hit points and add to multi-graph
  g_hitPos = rh.getFromFile(rootFile,'straw_calo_truth/%s/tracker/station_%i/g_hitPosTop_%s' % (particle,station,volume) )
  g_hitPos.SetMarkerColor(kRed)
  mg.Add(g_hitPos)

  #Draw multi-graph
  mg.Draw("AP")
  mg.SetTitle( g_birthPos.GetTitle() )
  mg.GetXaxis().SetTitle("Downstream pos (calo at left) [mm]")
  mg.GetYaxis().SetTitle("Radially inwards pos (ring towards bottom) [mm]")
  mg.GetXaxis().SetRangeUser(xRange[0],xRange[1])
  mg.GetYaxis().SetRangeUser(yRange[0],yRange[1])
  mg.GetYaxis().SetTitleOffset(1.5)

  raw_input("Press Enter to continue...")


#Plot desired graphs
gStyle.SetOptStat(0)
plotBirthAndHitPositionsFromChosenVolume("secondaries",0,"VacuumChamber",[-2000,7000],[-1000,8000])
plotBirthAndHitPositionsFromChosenVolume("secondaries",0,"Calo",[-1000,7000],[-1000,8000])
plotBirthAndHitPositionsFromChosenVolume("secondaries",0,"StrawManifold",[0,1200],[-500,1000])

