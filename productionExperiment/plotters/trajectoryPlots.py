from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="/home/tstuttard/g-2/gm2Dev_v6_02_00_StuttardMDC/data/StuttardTruthHistos.root", help='Input ROOT file containing plots from StuttardTrajectorySanityPlots module', dest='inputFile')
parser.add_argument('-n','--num-events-with-plots', type=int, required=True, dest='numEventsWithTrajPlots', help='Num events with trajectories plotted' )
args = parser.parse_args()


#Open input file
rootFile = rh.openFile(args.inputFile)

#
#Plot all decay e+ trajectories on same plot
#

gStyle.SetOptStat(0)

mg = TMultiGraph()

for i_event in range(0,args.numEventsWithTrajPlots) :

  #Add trajectory plot to multi graph
  gr = rh.getFromFile(rootFile,'trajectories/primary_e+/g_traj_evt%05i' % (i_event+1) )
  gr.SetMarkerStyle(7)
  mg.Add(gr)

  #Plot birth point
  birthPoint = TGraph(1)
  x = Double(0)
  y = Double(0)
  gr.GetPoint(0,x,y)
  birthPoint.SetPoint(0,x,y)
  birthPoint.SetMarkerStyle(4)
  birthPoint.SetMarkerColor(kGreen)
  mg.Add(birthPoint)
  
  #Plot death point
  birthPoint = TGraph(1)
  x = Double(0)
  y = Double(0)
  gr.GetPoint(gr.GetN()-1,x,y)
  birthPoint.SetPoint(0,x,y)
  birthPoint.SetMarkerStyle(4)
  birthPoint.SetMarkerColor(kRed)
  mg.Add(birthPoint)
  

#Draw multi graph
mg.Draw("APL")
mg.SetTitle('Decay positron trajectories;x global [mm];z global [mm]')
mg.GetXaxis().SetRangeUser(-1.5e4,1.5e4)
mg.GetYaxis().SetRangeUser(-1.5e4,1.5e4)
mg.GetYaxis().SetTitleOffset(1.3)
raw_input("Press Enter to continue...")

