#Make overall plots of individual GARFIELD runs

from ROOT import TFile, gROOT, TH1F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=True, help='Input ROOT file', dest='inputFile')
parser.add_argument('-n','--max-events', type=int, required=False, default=-1, help='Max num events to process', dest='maxNumEvents')
args = parser.parse_args()

#Open input file
rootFile = rh.openFile(args.inputFile)
if not rootFile : sys.exit(-1)

#Get event tree
t_event = rh.getFromFile(rootFile,"Garfield/Events")

#Get number of events to process
numEventsInFile = t_event.GetEntries()
numEventsToProcess = min(numEventsInFile,args.maxNumEvents) if args.maxNumEvents > 0 else numEventsInFile
print "Total events = %i : Processing  %i events" % (numEventsInFile,numEventsToProcess) 

#Init plotting


#
# Book histos
#

h_numThresholdCrossingsInEvent = TH1F("h_numThresholdCrossingsInEvent",";Num thresholds crossings in event", 6, -0.5, 5.5) 


#
# Event loop
#

#Plot raw signal for this event #TODO REMOVE
#t_event.Draw("rawSignalCurrent:rawSignalTime")
#raw_input("Press Enter to continue...")

#Loop over events
for i_evt in range(0,numEventsToProcess) :

  if i_evt % 100 == 0 : print "Event %i" % (i_evt)

  #Step tree to current event
  t_event.GetEntry(i_evt)


  #
  # Fill plots
  #

  h_numThresholdCrossingsInEvent.Fill(len(t_event.thresholdCrossingTimes))


#
# Draw plots
# 

h_numThresholdCrossingsInEvent.Draw()
raw_input("Press Enter to continue...")

