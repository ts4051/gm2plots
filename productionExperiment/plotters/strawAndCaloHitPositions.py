#Make nicer plots of calo and straw hit positions

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./truthPlots.root", help='Input ROOT file containing plots from StrawAndCaloTruthPlots module', dest='inputFile')
args = parser.parse_args()


#Open input file
rootFile = rh.openFile(args.inputFile)


#
# Compare two hit position plots
#

def plotHitTruthPositions(topPlotPath,topPlotTitle,bottomPlotPath,bottomPlotTitle) :

  #Create a fresh canvas
  c = TCanvas("c","",1200,800)
  c.Divide(1,2)

  #First hit plot
  h_primaryPositronHits = rh.getFromFile(rootFile,topPlotPath)
  c.cd(1)
  h_primaryPositronHits.SetTitle(topPlotTitle)
  #h_primaryPositronHits.GetYaxis().SetTitleOffset(1.5)
  h_primaryPositronHits.SetStats(False)
  h_primaryPositronHits.GetYaxis().SetRangeUser(-200.,400.)
  h_primaryPositronHits.Draw("COLZ")

  #Second hit plot
  h_secondaryHits = rh.getFromFile(rootFile,bottomPlotPath)
  c.cd(2)
  h_secondaryHits.SetTitle(bottomPlotTitle)
  #h_secondaryHits.GetYaxis().SetTitleOffset(1.5)
  h_secondaryHits.SetStats(False)
  h_secondaryHits.GetYaxis().SetRangeUser(-200.,400.)
  h_secondaryHits.Draw("COLZ")

  raw_input("Press Enter to continue...")



#
# Hit positions as trajectories
#

def plotHitTrajectories(particle,station) :

  gr = rh.getFromFile(rootFile,'straw_calo_truth/%s/station_%i/g_hitPosTop' % (particle,station) )

  gr.Draw("AP")
  gr.GetYaxis().SetTitleOffset(1.5)
  raw_input("Press Enter to continue...")


#
#Plot detector hit positions together
#

#Compare hit positions from primary e+ and secondaries (do for all stations)
stations = [0,12,18]
for station in stations :
  plotHitTruthPositions("straw_calo_truth/primary_e+/tracker/station_%i/h_hitPosTop_newBinning"%(station),"Hits from primary e+","straw_calo_truth/secondaries/tracker/station_%i/h_hitPosTop_newBinning"%(station),"Hits from secondaries")

#Compare hit positions for "all primary e+" vs "trackable primary e+" (do for all stations)
stations = [0,12,18]
for station in stations :
  plotHitTruthPositions("straw_calo_truth/primary_e+/tracker/station_%i/h_hitPosTop_newBinning"%(station),"Hits from ALL primary e+","straw_calo_truth/primary_e+/tracker/station_%i/trackable/h_hitPosTop_newBinning"%(station),"Hits from TRACKABLE primary e+")

#Plot detector hits as trajectories
gStyle.SetOptStat(0)
plotHitTrajectories("primary_e+",0)

