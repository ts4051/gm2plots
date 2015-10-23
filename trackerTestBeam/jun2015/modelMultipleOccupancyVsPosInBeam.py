import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.optimize import curve_fit
from scipy.stats import chi2
from sys import argv,exit
import datetime
from math import log10,pow,sqrt,fabs
from random import gauss,uniform
import argparse
#from ROOT import TFile, TCanvas, gStyle, TH1F, TH2F
import pylab

#
# Helper functions / classes
#

class Event :

  def __init__(self) :
    self.xVals = []
    self.yVals = []

  def addProton(self,x,y) :
    self.xVals.append(x)
    self.yVals.append(y)


class EventContainer :

  def __init__(self) :
    self.events = []

  def __len__(self) :
    return len(self.events)

  def add(self,event) :
    self.events.append(event)

  def addMany(self,events) :
    self.events.extend(events.events)

  def get(self,i) :
    return self.events[i]

  def getXVals(self):
    xVals = []
    for event in self.events : 
      for x in event.xVals : xVals.append(x)
    return xVals

  def getYVals(self):
    yVals = []
    for event in self.events :
      for y in event.yVals : yVals.append(y)
    return yVals

  def getSOEvents(self) :
    soEvents = EventContainer()
    for event in self.events :
      if len(event.xVals) == 1 : soEvents.add(event)
    return soEvents

  def getDOEvents(self) :
    doEvents = EventContainer()
    for event in self.events :
      if len(event.xVals) == 2 : doEvents.add(event)
    return doEvents


def getDOPosDiff(doEvent):
  xDiff = fabs( doEvent.xVals[1] - doEvent.xVals[0] )
  yDiff = fabs( doEvent.yVals[1] - doEvent.yVals[0] )
  return xDiff,yDiff


#
# Main
#

events = EventContainer()

# Generate events
numEvents = 100000
beamXRMS = 3.
beamYRMS = 3.
doubleOccProbability = 0.35
for i in xrange(0,numEvents,1):    

  event = Event()

  #Generate proton transverse position
  x = gauss(0.,beamXRMS)
  y = gauss(0.,beamYRMS)
  event.addProton(x,y)

  #Generate another proton if double occupancy event
  if uniform(0.,1.) < doubleOccProbability :

    #Generate proton transverse position
    x = gauss(0.,beamXRMS)
    y = gauss(0.,beamYRMS)
    event.addProton(x,y)

  #Add event to container
  events.add(event)


#Plot hits
plt.title('Beam transverse (cross-section) positions [mm]')
soEvents = events.getSOEvents()
plt.scatter(np.array(soEvents.getXVals()),np.array(soEvents.getYVals()),marker='.',c='blue')
doEvents = events.getDOEvents()
plt.scatter(np.array(doEvents.getXVals()),np.array(doEvents.getYVals()),marker='.',c='red')
plt.show()


#Plot displacement between hits in same bucket
xDiffs = []
yDiffs = []
for i in range(0,len(doEvents)) :
  doEvent = doEvents.get(i)
  xDiff,yDiff = getDOPosDiff(doEvent)
  xDiffs.append(xDiff)
  yDiffs.append(yDiff)
plt.title('x and y distance magnitude between protons from same bucket [mm]')
plt.scatter(np.array(xDiffs),np.array(yDiffs),marker='.',c='blue')
plt.show()

#Plot x vs x diff and y vs y diff
xVals = []
xDiffs = []
yVals = []
yDiffs = []
for i in range(0,len(doEvents)) :
  doEvent = doEvents.get(i)
  xDiff,yDiff = getDOPosDiff(doEvent)
  for x in doEvent.xVals :
    xVals.append(x)
    xDiffs.append(xDiff)
  for y in doEvent.yVals :
    yVals.append(y)
    yDiffs.append(yDiff)
#plt.title('Double occupancy protons: x vs x diff [mm]')
plt.scatter(np.array(xVals),np.array(xDiffs),marker='.',c='blue')
plt.xlabel('Double occupancy hit radial position (relative to beam center) [mm]')
plt.ylabel('Distance between double occupancy hits [mm]')
plt.show()
plt.title('Double occupancy protons: y vs y diff [mm]')
plt.scatter(np.array(yVals),np.array(yDiffs),marker='.',c='blue')
plt.show()

#Plot events with two protons within straw radius vs not
strawRadius = 5.
eventsGivingOneHitInSameStraw = EventContainer()
eventsGivingOneHitInSameStraw.addMany(soEvents) #all SO events leave just one hit per straw radius
eventsGivingTwoHitsInSameStraw = EventContainer()
for i in range(0,len(doEvents)) :
  doEvent = doEvents.get(i)
  xDiff,yDiff = getDOPosDiff(doEvent)
  if xDiff < strawRadius : eventsGivingTwoHitsInSameStraw.add(doEvent) 
  else : eventsGivingOneHitInSameStraw.add(doEvent) 
print "# events giving 1 hit same straw = %i , 2 hits = %i" % (len(eventsGivingOneHitInSameStraw),len(eventsGivingTwoHitsInSameStraw))
plt.title('x vs y (red points are problem DO) [mm]')
plt.scatter(np.array(eventsGivingOneHitInSameStraw.getXVals()),np.array(eventsGivingOneHitInSameStraw.getYVals()),marker='.',c='blue')
plt.scatter(np.array(eventsGivingTwoHitsInSameStraw.getXVals()),np.array(eventsGivingTwoHitsInSameStraw.getYVals()),marker='.',c='red')
plt.show()

#Compare x positons of protons producing <= 1 hit per straw to >1 hit per straw
oneHitInStrawBinCounts,oneHitInStrawBinEdges,patches = plt.hist(np.array(eventsGivingOneHitInSameStraw.getXVals()),bins=100, histtype='stepfilled')
pylab.setp(patches, 'facecolor', 'g', 'alpha', 0.5)
twoHitsInStrawBinCounts,twoHitsInStrawBinEdges,patches = plt.hist(np.array(eventsGivingTwoHitsInSameStraw.getXVals()),bins=100, histtype='stepfilled')
pylab.setp(patches, 'facecolor', 'r', 'alpha', 0.5)
plt.show()

# Create the histogram and normalize the counts to 1
oneHitInStrawHist, oneHitInStrawBins = np.histogram(eventsGivingOneHitInSameStraw.getXVals(), bins=50, range=(-15.,15.))
center = (oneHitInStrawBins[:-1]+oneHitInStrawBins[1:])/2
width = oneHitInStrawBins[1]-oneHitInStrawBins[0]
plt.bar(center, oneHitInStrawHist, align = 'center', width = width, color='blue', linewidth=0 )
twoHitsInStrawHist, twoHitsInStrawBins = np.histogram(eventsGivingTwoHitsInSameStraw.getXVals(), bins=50, range=(-15.,15.))
center = (twoHitsInStrawBins[:-1]+twoHitsInStrawBins[1:])/2
width = twoHitsInStrawBins[1]-twoHitsInStrawBins[0]
plt.bar(center, twoHitsInStrawHist, align = 'center', width = width, color='red', linewidth=0 )
plt.legend(['Events with <= 1 hit / straw','Events with > 1 hit / straw'])
plt.xlabel('Hit radial position (relative to beam center) [mm]')
plt.show()

#Ratio
ratios = []
for i in range(0,len(oneHitInStrawHist)) :
  ratio = float(oneHitInStrawHist[i]) / float(twoHitsInStrawHist[i]) if twoHitsInStrawHist[i]>0. else 0.
  ratios.append(ratio)
plt.plot(center, ratios)
plt.xlabel('Hit radial position (relative to beam center) [mm]')
plt.ylabel('Ratio : (<= 1 hit / straw) / (> 1 hit / straw)')
plt.show()
