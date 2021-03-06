#Combine trajectory plots for n events onto a single canvas
#Uses the output ROOT file from TrajectorySanityPlots module

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./trajectoryPlots.root", help='Input ROOT file containing plots from TrajectorySanityPlots module', dest='inputFile')
parser.add_argument('-nt','--num-events-total', type=int, required=True, dest='numEventsTotal', help='Num events')
parser.add_argument('-np','--num-events-to-plot', type=int, required=True, dest='numEventsToPlot', help='Num events with trajectories plotted' )
args = parser.parse_args()


#Open input file
rootFile = rh.openFile(args.inputFile)



#
# Functions for overlayign trajectories onto single plot
#

def combineAndPlotTrajectories(xaxis,yaxis) :

  mg = TMultiGraph()

  numTrajsPlotted = 0

  for i_event in range(0,args.numEventsTotal) :

    #Add trajectory plot to multi graph
    axesLabel = xaxis.capitalize() + yaxis.capitalize() #e.g. "x" and "y" -> "XY"
    gr = rh.getFromFile(rootFile,'trajectories/primary_e+/trajectories/g_traj%s_evt%05i' % (axesLabel,i_event+1), False )
    if not gr : continue #Skip if this event didn't return a trajectory (e.g. due to filters)
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

    #Break loop if have plotted enough
    numTrajsPlotted += 1
    if numTrajsPlotted >= args.numEventsToPlot: break
  
  print "Number of events plotted = %i" % (numTrajsPlotted)

  #Draw multi graph
  mg.Draw("APL")
  mg.SetTitle( "Decay positron trajectories;%s global [mm];%s global [mm]" % (xaxis,yaxis) )
  mg.GetXaxis().SetRangeUser(-1.5e4,1.5e4)
  mg.GetYaxis().SetRangeUser(-1.5e4,1.5e4)
  mg.GetYaxis().SetTitleOffset(1.5)
  raw_input("Press Enter to continue...")


#
#Plot all decay e+ trajectories on same plot
#

gStyle.SetOptStat(0)

#Plot for each 2D projection
combineAndPlotTrajectories("z","x")
combineAndPlotTrajectories("x","y")
combineAndPlotTrajectories("z","y")

