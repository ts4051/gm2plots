#Generic GARFIELD stuff

#
# Helper functions
#

#Get number of events to process
def getNumEventsToProcess(numEventsInFile,maxNumEventsFromUser,firstEventFromUser) :

  #First use num evnets in file and user first event only
  numEventsToProcess = numEventsInFile - firstEventFromUser
  if numEventsToProcess < 0 : 
    print "ERROR: First event to process %i is too large (%i events in file)" % (args.firstEvent,numEventsInFile)
    sys.exit(-1)

  #Next truncate by user max events
  if maxNumEventsFromUser > -1 :
    numEventsToProcess = min(numEventsInFile,maxNumEventsFromUser)

  #Report
  print "Total events = %i : Processing first %i events starting at event %i" % (numEventsInFile,numEventsToProcess,firstEventFromUser) 

  #Get maximum event number to process given args
  maxEventNumber = firstEventFromUser + numEventsToProcess

  #Return useful numbers
  return numEventsToProcess, firstEventFromUser, maxEventNumber


#Dump run info
def dumpRunInfo(t_runInfo) :

  print "\nRun info :"
  print "  ASDQ threshold = %f [mV]" % (t_runInfo.asdqThresholdmV)
  #TODO particle name
  print "  Track momentum = %f [GeV]" % (t_runInfo.trackMomentum/1.e9) #eV -> GeV
  print ""

