import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.optimize import curve_fit
from scipy.stats import chi2,norm
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

#Track fit (where Z is known for sure, e.g. station positions)
def trackFitKnownZ(trackPoints) :

  #Get means
  xMean = np.mean(getXList(trackPoints))
  yMean = np.mean(getYList(trackPoints))
  zMean = np.mean(getZList(trackPoints))

  #Get gradients
  denom = 0 ; nomY = 0. ; nomX = 0.0
  sdX = 0 ; sdY = 0. ; sdZ = 0.0
  for pos in trackPoints :
    sdX += ( pos.x - xMean )
    sdY += ( pos.y - yMean )
    sdZ += ( pos.z - zMean )
    nomX += sdZ * sdX;
    nomY += sdZ * sdY;
    denom += sdZ * sdZ;
  gradientX = nomX / denom;
  gradientY = nomY / denom;

  #Get intercepts
  interceptX = xMean - (gradientX * zMean);
  interceptY = yMean - (gradientY * zMean);

  #Get track (from first and last Z points)
  track = list()
  track.append( Pos(x=(interceptX+(gradientX*trackPoints[0].z)), \
                    y=(interceptY+(gradientY*trackPoints[0].z)), \
                    z=trackPoints[0].z) )
  track.append( Pos(x=(interceptX+(gradientX*trackPoints[-1].z)), \
                    y=(interceptY+(gradientY*trackPoints[-1].z)), \
                    z=trackPoints[-1].z) )

  #Get residuals
  xResiduals = list()
  yResiduals = list()
  for pos in trackPoints :
    xResiduals.append( pos.x - interceptX + (gradientX * pos.z) )
    yResiduals.append( pos.y - interceptY + (gradientY * pos.z) )

  return track, xResiduals, yResiduals


#
# Main
#

beamPosUm = list()

# Generate tracks
numEvents = 10000
beamXRMSUm = 3000.
beamYRMSUm = 3000.
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
strawModuleResolutionUm = 200.

#Define silicon
stripPitchUm = 80.
stationResolution = stripPitchUm / math.sqrt(12.)
siliconStationsTruthHitsZUm = [-2.e6, -1e6, 1.e6, 2.e6 ] #TODO Does it matter to use real values? 

#Get straw hit positions from beam
strawHits = list()
strawSmearedHits = list()
for beamPos in beamPosUm :

  #Truth hit
  strawHits.append( Pos(x=beamPos.x,y=beamPos.y,z=strawsZUm) )

  #Smeared hit
  strawSmearedHits.append( Pos(x=gauss(beamPos.x,strawModuleResolutionUm), \
                               y=gauss(beamPos.y,strawModuleResolutionUm), \
                               z=strawsZUm ) ) 

#Plot truth hits
fig = plt.figure()
plt.suptitle('Truth hit positions')
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
plt.suptitle('Smeared silicon hit positions')
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

#Fit track to silicon hits
xResiduals = list()
yResiduals = list()
dcaResiduals = list()
tracks = list()
for i_hit in range(0,len(siliconStationsHits[0])) : #Loop over hits

  #Fit track
  hits = list()
  for i_station in range(0,len(siliconStationsHits)) : #Loop over station
    hits.append( siliconStationsHits[i_station][i_hit] )
  track, trackXResiduals, trackYResiduals = trackFitKnownZ(hits)
  tracks.append(track)

  #Store residuals
  xResiduals.extend(trackXResiduals)
  yResiduals.extend(trackYResiduals)

  #Compute DCA residuals
  for i_res in range(0,len(trackXResiduals)) :
    dcaResiduals.append( math.sqrt( math.pow(trackXResiduals[i_res],2.) + math.pow(trackYResiduals[i_res],2.) ) )

  '''
  #Plot this track
  fig = plt.figure()
  plt.suptitle('Event %i reco track'%(i_hit))
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter(getXList(hits),getYList(hits),getZList(hits), c='g', marker='.')
  ax.plot([track[0].x,track[1].x],[track[0].y,track[1].y],zs=[track[0].z,track[1].z],c='r')
  plt.show()
  '''

#Plot the x residuals (with Gaussian fit)
n,bins,patches = plt.hist(np.array(xResiduals),bins=100,normed=True)
(mu, sigma) = norm.fit(xResiduals)
plt.plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2)
plt.title('Fit x residuals : mean=%f sigma=%f : [um]'%(mu,sigma))
plt.show()

#Plot the y residuals (with Gaussian fit)
n,bins,patches = plt.hist(np.array(yResiduals),bins=100,normed=True)
(mu, sigma) = norm.fit(yResiduals)
plt.plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2)
plt.title('Fit y residuals : mean=%f sigma=%f : [um]'%(mu,sigma))
plt.show()

#Plot total DCA residual
plt.hist(np.array(dcaResiduals),bins=100,normed=True)
plt.title('Fit residual magnitudes : [um]')
plt.show()

#Find residuals to truth
truthXResiduals = list()
truthYResiduals = list()
truthDCAResiduals = list()
for i_track in range(0,len(tracks)) :
  for pt in tracks[i_track] :
    truthXResiduals.append( pt.x - beamPosUm[i_track].x )
    truthYResiduals.append( pt.y - beamPosUm[i_track].y )
    truthDCAResiduals.append( math.sqrt( math.pow(truthXResiduals[-1],2.) + math.pow(truthYResiduals[-1],2.) ) )

#Plot the truth x residuals (with Gaussian fit)
n,bins,patches = plt.hist(np.array(truthXResiduals),bins=100,normed=True)
(mu, sigma) = norm.fit(truthXResiduals)
plt.plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2)
plt.title('Truth x residuals : mean=%f sigma=%f : [um]'%(mu,sigma))
plt.show()

#Plot the truth y residuals (with Gaussian fit)
n,bins,patches = plt.hist(np.array(truthYResiduals),bins=100,normed=True)
(mu, sigma) = norm.fit(truthYResiduals)
plt.plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2)
plt.title('Truth y residuals : mean=%f sigma=%f : [um]'%(mu,sigma))
plt.show()

#Plot the truth DCA residuals (with Gaussian fit)
n,bins,patches = plt.hist(np.array(truthDCAResiduals),bins=100,normed=True)
plt.title('Truth residual magnitudes : [um]')
plt.show()

#TODO residuals to smeared straw hit

