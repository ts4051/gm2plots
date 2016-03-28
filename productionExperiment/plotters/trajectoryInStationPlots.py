#Combine trajectory in straw+calo stations plots for n events onto a single canvas
#Uses the output ROOT file from StrawAndCaloTruthPlots module

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./truthPlots.root", help='Input ROOT file containing plots from StrawAndCaloTruthPlots module', dest='inputFile')
parser.add_argument('-nt','--num-events-total', type=int, required=True, dest='numEventsTotal', help='Num events')
parser.add_argument('-np','--num-events-to-plot', type=int, required=True, dest='numEventsToPlot', help='Num events with trajectories plotted' )
parser.add_argument('-t','--trackable', action="store_true", dest='trackable', default=False, help='Plot trackable trajectories only' )
parser.add_argument('-e','--specify-event', type=int, required=False, dest='chosenEvent', default=-1, help='Specify event')
args = parser.parse_args()

#Open input file
rootFile = rh.openFile(args.inputFile)


#
# Functions for overlaying trajectories onto single plot
#

def combineAndPlotTrajectories(station,perspective,yMin,yMax) :

  mg = TMultiGraph()

  numTrajsPlotted = 0

  #Add "trackable" to path if arg set
  rootDirName = "straw_calo_truth/primary_e+/station_%i" % (station)
  if args.trackable : rootDirName += "/trackable"
  rootDirName += "/trajectories"

  for i_event in range(0,args.numEventsTotal) :

    if args.chosenEvent > 0 :
      if i_event != args.chosenEvent : continue

    #Add trajectory plot to multi graph
    name = rootDirName + "/g_trajInStation%s_evt%05i" % (perspective,i_event+1)
    gr = rh.getFromFile(rootFile,name,False)
    if not gr : continue #Skip if this event didn't return a trajectory (e.g. due to filters)
    gr.SetMarkerStyle(8)
    gr.SetMarkerSize(1)
    mg.Add(gr)

    print "Using event %i" % (i_event)

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

    #Store first graph so can copy titles etc later
    if numTrajsPlotted == 0 :
      storedGraph = gr

    #Break loop if have plotted enough
    numTrajsPlotted += 1
    if numTrajsPlotted >= args.numEventsToPlot: break

  if numTrajsPlotted == 0 : 
    print "No trajectories plotted for \"%s\" perspective in station %i" % (perspective,station)
    return

  print "Number of events plotted = %i" % (numTrajsPlotted)

  #Draw multi graph
  mg.Draw("APL")
  #mg.GetXaxis().SetRangeUser(xMin,xMax) #TODO Can't make larger that range in point x values, FIXME Can this be forced before filling?
  mg.GetYaxis().SetRangeUser(yMin,yMax)
  mg.GetXaxis().SetTitle( storedGraph.GetXaxis().GetTitle() ) #Get axis titles from one of the individual graphs
  mg.GetYaxis().SetTitle( storedGraph.GetYaxis().GetTitle() )
  mg.GetYaxis().SetTitleOffset(1.2)
  mg.GetYaxis().SetTitleOffset(1.5)
  mg.SetTitle( "Decay positron trajectories in station %i (using straw hit positions) : %s" % (station,perspective) )
  mg.Draw("APL")
  raw_input("Press Enter to continue...")


#
#Plot all decay e+ trajectories on same plot
#

gStyle.SetOptStat(0)

#Define stations
stations = [0,12,18]

#Plot for each 2D projection
for station in stations :
  combineAndPlotTrajectories(station,"Top",-200.,250.)
#  combineAndPlotTrajectories(station,"Top",-400.,900.)
  combineAndPlotTrajectories(station,"Downstream",-300.,200.)
  combineAndPlotTrajectories(station,"Side",-650,650)

