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
import collections
from mpl_toolkits.mplot3d import Axes3D
import math

#
# Helper functions
#

#Calculate distance of closest approach of a line to a point
def dca(start,end,point):

    xDelta = end[0] - start[0]
    yDelta = end[1] - start[1]

    m = yDelta/xDelta
    c  = end[1] - m*end[0]

    if ((xDelta == 0) and (yDelta == 0)):
      raise ValueError('dca : xDelta and yDelta are both ZERO')

    u = ( (point[0] - start[0])*xDelta + (point[1] - start[1])*yDelta ) / (xDelta*xDelta + yDelta*yDelta)

    if (u < 0):
      closestPoint = [start[0], start[1]]
    elif (u > 1):
      closestPoint = [end[1], end[1]]
    else:
      closestPoint = [ start[0]+u*xDelta,  start[1]+u*yDelta]

    dx = closestPoint[0] - point[0]
    dy = closestPoint[1] - point[1]
    
    if (dy >= 0):
      sign = -1
    else:
      sign = +1

    dcaV = sign*sqrt(dx*dx +dy*dy)

    return dcaV


#Straight line function for fitting
def straight_line_fit(z, a, b):
  return a + b*z


#Gaussian function for fitting
def gaussian_fit(x,A,mu,sigma):
  return A*np.exp(-(x-mu)**2/(2.*sigma**2))

#Track/hit position
Pos = collections.namedtuple('Pos', 'x y z')

#Get single coord list form Pos list
def getXList(posList) :
  xList = list()
  for pos in posList : xList.append(pos.x)
  return xList

def getYList(posList) :
  yList = list()
  for pos in posList : yList.append(pos.y)
  return yList

def getZList(posList) :
  zList = list()
  for pos in posList : zList.append(pos.z)
  return zList


#
# Main
#

beamPosUm = list()

# Generate tracks
numEvents = 10000
beamXRMSUm = 100.
beamYRMSUm = 100.
for i in xrange(0,numEvents,1):    

  #Generate beam start point
  x = gauss(0.,beamXRMSUm)
  y = gauss(0.,beamYRMSUm)
  beamPosUm.append( Pos(x=x,y=y,z=0.) )

#Plot beam
plt.title('Beam transverse (cross-section) positions [um]')
plt.scatter(getXList(beamPosUm),getYList(beamPosUm),marker='.',c='blue')
plt.show()

#Define straws
strawsZUm = 0.

#Define silicon
stripPitchUm = 80.
stationResolution = stripPitchUm / math.sqrt(12.)
siliconStationsTruthHitsZUm = [-4000., -2000., 2000., 4000. ] #TODO Does it matter to use real values? 

#Get straw hit truth positions from beam
strawHits = list()
for beamPos in beamPosUm :
  strawHits.append( Pos(x=beamPos.x,y=beamPos.y,z=strawsZUm) )

#Plot truth hits
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(getXList(strawHits),getYList(strawHits),getZList(strawHits), c='r', marker='.')
ax.set_xlabel('Hit x [um]')
ax.set_ylabel('Hit y [um]')
ax.set_zlabel('Hit z [um]')

#Get silicon hit truth positions from beam
siliconStationsTruthHits = dict()
for i_station in range(0,len(siliconStationsTruthHitsZUm)) :
  siliconTruthHits = list()
  for beamPos in beamPosUm :
    siliconTruthHits.append( Pos(x=beamPos.x,y=beamPos.y,z=siliconStationsTruthHitsZUm[i_station]) )
  siliconStationsTruthHits[i_station] = siliconTruthHits

  #Plot truth hits
  ax.scatter(getXList(siliconTruthHits),getYList(siliconTruthHits),getZList(siliconTruthHits), c='b', marker='.')

#Show the 3D truth hits plot  
plt.show()

#Prepare plot for smeared hits
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Hit x [um]')
ax.set_ylabel('Hit y [um]')
ax.set_zlabel('Hit z [um]')

#Smear silicon hits by resolution
siliconStationsHits = dict()
for i_station in range(0,len(siliconStationsTruthHits)) :
  siliconHits = list()
  for truthHit in siliconStationsTruthHits[i_station] :
    siliconHits.append( Pos(x=gauss(truthHit.x,stationResolution),y=gauss(truthHit.y,stationResolution),z=truthHit.z) )
  siliconStationsHits[i_station] = siliconHits

  #Plot smeared hits
  ax.scatter(getXList(siliconHits),getYList(siliconHits),getZList(siliconHits), c='g', marker='.')

#Show the 3D smeared hits plot  
plt.show()



