#Model track rates
#Tom Stuttard (31st Oct 2016) 

import numpy as np
import sys, datetime, math, random, argparse
#import pylab
import matplotlib.pyplot as plt
import mathtools


#
# Define generic/common params
#

#The boards
numTDCChannels = 16
numTDCsPerLB = 4
numLBsPerFC7 = 16
numFC7sPerStation = 1
numStations = 3

frontendBoardWordSize = 32 #Bits
amc13WordSize = 64 #Bits
numWordsInTDCHeader = 32
numWordsInLBHeaderAndFooter = 13 #TODO CHECK
numWordsInLBChannelHeader = 4
numWordsInFC7EventHeader = 8
numWordsInFC7DDR3Padding = 7 #Really 0-7
numWordsInAMCHeaderAndFooter = 3
numWordsInAMCPayloadBlockHeader = 1 #TODO Handle payload blocks
numWordsInAMC13PayloadBlockHeaderAndFooter = 2 #TODO Handle payload blocks
numWordsInAMC13HeaderAndFooter = 3

#Physics constants
speedOfLightMperS = 299792458. #CODATA 2014
muonAnomaly = 11659203.e-10 #E821 value
muonRestMassGeV = 105.6583715e-3 #PDG 2014
muonRestLifetimeNs = 2.1969811e3 #PDG 2014
electronChargeC = 1.602176487e-19 #PDG 2011


#
# Helper functions
#

def getTDCEventSize(numHitWordsInTDC) :
  numWordsInTDCEvent = numWordsInTDCHeader + numHitWordsInTDC
  numBitsInTDCEvent = frontendBoardWordSize * numWordsInTDCEvent
  return numWordsInTDCEvent,numBitsInTDCEvent


def getLBEventSize(numHitWordsInTDC) :
  numWordsInTDCEvent,numBitsInTDCEvent = getTDCEventSize(numHitWordsInTDC)
  numWordsInLBEvent = numWordsInLBHeaderAndFooter + ( numTDCsPerLB * numWordsInTDCEvent )
  numBitsInLBEvent = frontendBoardWordSize * numWordsInLBEvent
  return numWordsInLBEvent,numBitsInLBEvent


def getAMCEventSize(numHitWordsInTDC) :
  numWordsInLBEvent,numBitsInLBEvent = getLBEventSize(numHitWordsInTDC)
  numWordsInFC7Event = ( ( numWordsInLBEvent + numWordsInLBChannelHeader ) * numLBsPerFC7 ) + numWordsInFC7EventHeader + numWordsInFC7DDR3Padding #32-bit
  numWordsInAMCEvent = numWordsInAMCHeaderAndFooter + numWordsInAMCPayloadBlockHeader + math.ceil(float(numWordsInFC7Event)/2.) #64-bit
  numBitsInAMCEvent = numWordsInAMCEvent * amc13WordSize
  return numWordsInAMCEvent, numBitsInAMCEvent


def getAMC13EventSize(numHitWordsInTDC) :
  numWordsInAMCEvent,numBitsInAMCEvent = getAMCEventSize(numHitWordsInTDC) #64-bit
  numWordsInAMC13Event = numWordsInAMCHeaderAndFooter + numWordsInAMC13PayloadBlockHeaderAndFooter + ( numWordsInAMCEvent * numFC7sPerStation * numStations )
  numBitsInAMC13Event = numWordsInAMC13Event * amc13WordSize
  return numWordsInAMC13Event, numBitsInAMC13Event


#
# One muon simulation
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  
  #
  # Define params
  #

  #Accelerator
  numFillsPerShortBatch = 8
  timeBetweenFillsInShortBatchMs = 10.
  numShortBatchesPerSuperCycle = 2
  timeBetweenShortBatchesInSuperCycleMs = 197.
  superCycleLengthS = 1.33

  #Beam
  #TODO

  #DAQ
  tdcBufferSize = 2016
  tdcToLBDataRateBitPerS = 2.5e6 * 8. #8b/10b, 25Mbps of raw data and 2.5MBytes/s of real data
  lbToFC7DataRateBitPerS = 12.5e6 * 8. #8b/10b via fiber, 125Mbps of raw data and 12.5MBytes/s of real data
  amcToAMC13DataRateBitPerS = 5.e9 #8b10/10b via uTCA backplane, 5Gbit
  amc13ToPCDataRateBitPerS = 5.e9 #GbEth fiber DAQ link from AMC13 to PC
  accumulationDurationMs = 2.
  bothEdges = False

  #Report
  print ""
  print "Params:"
  print "  Accumulation window = %f ms" % (accumulationDurationMs)
  print "  Both edges = %i" % (bothEdges)
  print "  TDC   -> LB    data rate = %f Mb/s" % (tdcToLBDataRateBitPerS*1.e-6) 
  print "  LB    -> FC7   data rate = %f Mb/s" % (lbToFC7DataRateBitPerS*1.e-6) 
  print "  FC7   -> AMC13 data rate = %f Mb/s" % (amcToAMC13DataRateBitPerS*1.e-6) 
  print "  AMC13 -> PC    data rate = %f Mb/s" % (amc13ToPCDataRateBitPerS*1.e-6) 
  print ""


  #
  # Fill rate due to accelerator fill structure
  #

  print ""
  print "Rates due to fill structure :"

  numFillsPerSuperCycle = numFillsPerShortBatch * numShortBatchesPerSuperCycle
  averageNumFillsPerS = float(numFillsPerSuperCycle) / superCycleLengthS
  averageGapBetweenFillsS = 1. / averageNumFillsPerS
  timeSpentAccumulatingPerSuperCycleMs = float(numFillsPerSuperCycle) * accumulationDurationMs
  averageTimeForReadoutPerFillS = ( superCycleLengthS - (timeSpentAccumulatingPerSuperCycleMs*1.e-3) ) / float(numFillsPerSuperCycle)
  shortestTimeForReadoutMs = timeBetweenFillsInShortBatchMs - accumulationDurationMs

  print "  Num fills per supercycle = %i" % (numFillsPerSuperCycle)
  print "  Averaged rate of fills = %f Hz" % (averageNumFillsPerS)
  print "  Averaged gap = %f ms" % (averageGapBetweenFillsS*1.e3)
  print "  Averaged time for readout per fill = %f ms" % (averageTimeForReadoutPerFillS*1.e3)
  print "  Shortest gap = %f ms" % (timeBetweenFillsInShortBatchMs)
  print "  Shortest gap for readout = %f ms" % (shortestTimeForReadoutMs)

  print ""


  #
  # Max possible rates due to electronics constraints
  #

  #Max rate vs TDC buffer filling
  #LB is 8b10b copy is the bottle-neck (TODO true? also calculate for AMC13)

  print ""
  print "Max rates due to electronics constraints :"

  #Loop over buffer filling value
  for percentFilled in np.arange(0.,125.,25.) :

    #TODO Consider processing time in boards?

    #Generate TDC buffer size
    numHitsInTDCBuffer = (percentFilled/100.) * float(tdcBufferSize)

    #TDC -> LB send time
    numWordsInTDCEvent,numBitsInTDCEvent = getTDCEventSize(numHitsInTDCBuffer) 
    tdcEventSendTimeMs = 1.e3 * float(numBitsInTDCEvent) / float(tdcToLBDataRateBitPerS)

    #LB to FC7 send time (only worry about for one as parallelised)
    numWordsInLBEvent,numBitsInLBEvent = getLBEventSize(numHitsInTDCBuffer) 
    lbEventSendTimeMs = 1.e3 * float(numBitsInLBEvent) / float(lbToFC7DataRateBitPerS)

    #Overall time taken from trigger to event in AMC13 (where buffering can occur)
    endAccumulationToEventInFC7TimeMs = tdcEventSendTimeMs + lbEventSendTimeMs
    triggerToEventInFC7TimeMs = accumulationDurationMs + endAccumulationToEventInFC7TimeMs

    #FC7 to AMC13 send time (only worry about for one as parallelised)
    numWordsInAMCEvent,numBitsInAMCEvent = getAMCEventSize(numHitsInTDCBuffer)
    amcEventSendTimeMs = 1.e3 * float(numBitsInAMCEvent) / float(amcToAMC13DataRateBitPerS)

    #Overall time taken from trigger to event in AMC13 (where buffering occurs)
    endAccumulationToEventInAMC13TimeMs = endAccumulationToEventInFC7TimeMs + amcEventSendTimeMs
    triggerToEventInAMC13TimeMs = triggerToEventInFC7TimeMs + amcEventSendTimeMs

    #Also add data send to PC time (not part of bottleneck due to buffering but still relevent)
    numWordsInAMC13Event,numBitsInAMC13Event = getAMC13EventSize(numHitsInTDCBuffer)
    amc13EventSendTimeMs = 1.e3 * float(numBitsInAMCEvent) / float(amc13ToPCDataRateBitPerS)

    #Overall time taken from trigger to event in PC (ignoring buffering)
    triggerToEventInPCTimeMs = triggerToEventInAMC13TimeMs + amc13EventSendTimeMs

    print ""
    print "  TDC buffer filling = %f %% (%i hit words per TDC):"% (percentFilled,numHitsInTDCBuffer)

    print ""

    print "    TDC event to LB send time (8b/10b) = %f ms (%i 32-bit words)" % (tdcEventSendTimeMs,numWordsInTDCEvent)
    print "    LB event to FC7 send time (fiber 8b/10b) = %f ms (%i 32-bit words)" % (lbEventSendTimeMs,numWordsInLBEvent)
    print "    FC7/AMC event to AMC13 send time (uTCA backplane) = %f ms (%i 64-bit words)" % (amcEventSendTimeMs,numWordsInAMCEvent)
    print "    AMC13 event to PC send time (DAQ fiber) = %f ms (%i 64-bit words)" % (amc13EventSendTimeMs,numWordsInAMC13Event)

    print ""

    print "    Time from end of TDC accumulation to data in FC7 buffer = %f ms" % (endAccumulationToEventInFC7TimeMs)
    print "    Time from end of TDC accumulation to data in AMC13 buffer = %f ms" % (endAccumulationToEventInAMC13TimeMs)

    print ""

    print "    Time from trigger to data in FC7 buffer (includes fill length) = %f ms" % (triggerToEventInFC7TimeMs)
    print "    Time from trigger to data in AMC13 buffer (includes fill length) = %f ms" % (triggerToEventInAMC13TimeMs)
    print "    Time from trigger to data in PC (includes fill length) = %f ms" % (triggerToEventInPCTimeMs)

    print ""

    #Alternatively thnk about avereage bit rate from AMC13 to PC
    averageAMC13DataRateBitsPerS = numBitsInAMC13Event * averageNumFillsPerS

    print "    Total tracker data volume = %i [64-bit words] = %f [Mb]" % (numWordsInAMC13Event,numWordsInAMC13Event*amc13WordSize*1.e-6)
    print "    Total tracker AMC13 average data rate = %f [Mb/s]" % (averageAMC13DataRateBitsPerS*1.e-6)
 
  print ""


  #
  # What does a full TDC buffer mean?
  #

  print ""
  print "Meaning of a full TDC buffer :"

  numHitWordsPerChannel = float(tdcBufferSize) / float(numTDCChannels)

  print "  %i hits per straw per fill (%i if recording both edges)" % (math.floor(numHitWordsPerChannel),math.floor(numHitWordsPerChannel/2.))
 
  print ""


