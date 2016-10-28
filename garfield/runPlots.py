#Make overall plots of individual GARFIELD runs
#Tom Stuttard

from ROOT import TFile, gROOT, TH1F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree
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
  parser.add_argument('-s','--event-step', type=int, required=False, default=1, help='Num events to step', dest='eventStep')
  args = parser.parse_args()

  #Open input file
  rootFile = rh.openFile(args.inputFile)
  if not rootFile : sys.exit(-1)

  #Init plotting
  gStyle.SetOptStat(0)

  #
  # Book histos
  #

  h_numThresholdCrossingsInEvent = TH1F("h_numThresholdCrossingsInEvent",";Num thresholds crossings in event", 6, -0.5, 5.5) 

  h_positiveThresholdCrossingTime = TH1F("h_positiveThresholdCrossingTime",";Positive threshold crossing time [ns]", 100, 0., 200.) 


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

  #Get events numbers to process
  eventNums = gh.getEventNumsToProcess(t_event.GetEntries(),args.maxNumEvents,args.firstEvent,args.eventStep)

  #Plot raw signal for this event #TODO REMOVE
  #t_event.Draw("rawSignalCurrent:rawSignalTime")
  #raw_input("Press Enter to continue...")

  #Loop over events
  for i_evt in eventNums :

    if i_evt % 100 == 0 : print "Event %i" % (i_evt) #TODO % done instead

    #Step tree to current event
    t_event.GetEntry(i_evt)


    #
    # Fill plots
    #

    h_numThresholdCrossingsInEvent.Fill( len(t_event.thresholdCrossingTimes) )

    if len(t_event.thresholdCrossingTimes) == 2 : #TODO Need to record threshold crossing direction, is what I'm doing here sensible?
      h_positiveThresholdCrossingTime.Fill( t_event.thresholdCrossingTimes[0] )


  #
  # Draw plots
  # 

  h_numThresholdCrossingsInEvent.Draw()
  raw_input("Press Enter to continue...")

  h_positiveThresholdCrossingTime.Draw()
  raw_input("Press Enter to continue...")

