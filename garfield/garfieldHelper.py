#Generic GARFIELD stuff
#Import into plotters
#Tom Stuttard

import math
import numpy as np

#
# Helper functions
#

#Get event numbers to process
def getEventNumsToProcess(numEventsInFile,maxNumEventsFromUser,firstEventFromUser,eventStepSizeFromUser) :

  #First use num events in file and user first event only
  numEventsToProcess = numEventsInFile - firstEventFromUser
  if numEventsToProcess < 0 : 
    print "ERROR: First event to process %i is too large (%i events in file)" % (args.firstEvent,numEventsInFile)
    sys.exit(-1)

  #Figure out max num steps possible according to first event and step size
  numEventsInSteps = math.floor( float(numEventsToProcess) / float(eventStepSizeFromUser) )

  #Next truncate by user max events
  if maxNumEventsFromUser > -1 :
    numEventsToProcess = min(numEventsInSteps,maxNumEventsFromUser)

  #Report
  print "Total events = %i : Processing first %i events starting at event %i in steps of %i" \
    % (numEventsInFile,numEventsToProcess,firstEventFromUser,eventStepSizeFromUser) 

  #Get maximum event number to process given args
  maxEventNumber = firstEventFromUser + (numEventsToProcess * eventStepSizeFromUser)

  #Return the event numbers (as ints)
  return [ int(i) for i in np.arange(firstEventFromUser,maxEventNumber,eventStepSizeFromUser) ]



#Dump run info
def dumpRunInfo(t_runInfo) :

  print "\nRun info :"
  print "  ASDQ threshold = %f [mV]" % (t_runInfo.asdqThresholdmV)
  #TODO particle name
  print "  Track momentum = %f [GeV]" % (t_runInfo.trackMomentum/1.e9) #eV -> GeV
  print ""

