#Generic GARFIELD stuff
#Import into plotters
#Tom Stuttard

import math, sys
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
  print "Total events = %i : Processing %i events starting at event %i in steps of %i" \
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


#Check track params
#Plotters make some assumptions so want to confim they are valid
def checkTrack(trackTime,trackOrigin,trackDirection) :

  tolerance = 1.e-6

  #Track time should be 0 ns
  if trackTime > tolerance :
    print "Track time = %f ns, expected 0 ns" % (trackTime)
    sys.exit(-1)

  #Track origin should be to the left of the straw, and in the plane z = 0 
  if trackOrigin.x() < -0.25 : #To the left of the straw
    print "Track origin not to left of straw"
    sys.exit(-1)

  if abs(trackOrigin.z()) > tolerance :
    print "Track origin not in z = 0 plane"
    sys.exit(-1)

  #Track direction should be +x 
  if abs(trackDirection.x()-1.) > tolerance or \
     abs(trackDirection.y()) > tolerance or \
     abs(trackDirection.z()) > tolerance :
    print "Track not travelling in +x"
    sys.exit(-1)

