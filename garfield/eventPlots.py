#Make plots of individual GARFIELD events

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree
import os, argparse, math, sys
import RootHelper as rh
import garfieldHelper as gh

#
# Main function
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #Get args
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('-i','--input-file', type=str, required=True, help='Input ROOT file', dest='inputFile')
  parser.add_argument('-n','--max-events', type=int, required=False, default=-1, help='Max num events to process', dest='maxNumEvents')
  parser.add_argument('-e','--first-event', type=int, required=False, default=0, help='First event to process', dest='firstEvent')
  args = parser.parse_args()

  #Open input file
  rootFile = rh.openFile(args.inputFile)
  if not rootFile : sys.exit(-1)

  #Init plotting
  gStyle.SetOptStat(0)


  #
  # Run info
  #

  #Get run info tree
  t_runInfo = rh.getFromFile(rootFile,"Garfield/RunInfo")
  t_runInfo.GetEntry(0) #Only one entry

  #Dump some print
  gh.dumpRunInfo(t_runInfo)


  #
  # Event loop
  #

  #Get event tree
  t_event = rh.getFromFile(rootFile,"Garfield/Events")

  #Get number of events to process
  numEventsToProcess,firstEventNumber,maxEventNumber = gh.getNumEventsToProcess(t_event.GetEntries(),args.maxNumEvents,args.firstEvent)

  #Loop over events
  for i_evt in range(firstEventNumber,maxEventNumber) :

    print "\n\n---------------------------------------------"
    print "Event %i :" % (i_evt)

    #Step tree to current event
    t_event.GetEntry(i_evt)


    #
    # Report basic info
    #

    print "  Num clusters = %i" % (t_event.numClusters)
    print "  Num threshold crossing = %i" % (len(t_event.thresholdCrossingTimes))
    print ""


    #
    # Plot raw signal
    #

    numPoints = len(t_event.rawSignalTime)
    g_rawSignal = TGraph(numPoints)
    g_rawSignal.SetTitle( "Event %i : Raw signal ; Time [ns] ; Current [#mu A]" % i_evt )
  
    for i_pt in range(0,numPoints) :
      g_rawSignal.SetPoint(i_pt,t_event.rawSignalTime[i_pt],t_event.rawSignalCurrent[i_pt])

    g_rawSignal.Draw("APL")

    raw_input("Press Enter to continue...")


    #
    # Plot shaped signal
    #

    mg_shapedSignal = TMultiGraph()

    #First plot the shaped signal...

    numPoints = len(t_event.shapedSignalTime)
    g_shapedSignal = TGraph(numPoints)
  
    for i_pt in range(0,numPoints) :
      g_shapedSignal.SetPoint(i_pt,t_event.shapedSignalTime[i_pt],t_event.shapedSignalVoltage[i_pt])

    mg_shapedSignal.Add(g_shapedSignal)

    #g_shapedSignal.Draw("APL")

    #Then superimpose with threshold crossing points...

    numPoints = len(t_event.thresholdCrossingTimes)
    if numPoints > 0:

      g_thresholdsCrossings = TGraph(numPoints)
      for i_pt in range(0,numPoints) :
        g_thresholdsCrossings.SetPoint(i_pt,t_event.thresholdCrossingTimes[i_pt],t_event.thresholdCrossingLevels[i_pt])

      g_thresholdsCrossings.SetMarkerStyle(24)
      g_thresholdsCrossings.SetLineColor(2)
      g_thresholdsCrossings.SetMarkerColor(2)

      mg_shapedSignal.Add(g_thresholdsCrossings)

    else:
      print "No threshold crossings, so not adding to plot"

    mg_shapedSignal.SetTitle( "Event %i : Shaped signal ; Time [ns] ; Voltage [mV]" % i_evt )
    mg_shapedSignal.Draw("APL")

    raw_input("Press Enter to continue...")


