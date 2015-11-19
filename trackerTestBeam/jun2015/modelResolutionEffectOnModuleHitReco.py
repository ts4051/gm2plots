import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.optimize import curve_fit
from scipy.stats import chi2, norm
from sys import argv,exit
import datetime
from math import log10,pow,sqrt,fabs
from random import gauss,uniform
import argparse
import collections 
import math

#Everything in this script is in y-z plane
#Lines defined by z = my + c
#All distance units in [um]


'''
Helper functions and structures
'''

#Define structs
Coord = collections.namedtuple('Coord', 'y z')
Line = collections.namedtuple('Line', 'm c')

#Get points on line
def getLineZ(y,line):
  z = line.m*y + line.c
  return z

def getLineY(z,line):
  y = (z-line.c)/line.m
  return y

#Get line end points
def getLineEndsFromZ(z1,z2,line):
  zVals = [z1,z2]
  yVals = [ getLineY(zVals[0],line) , getLineY(zVals[1],line) ]
  return yVals,zVals


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


'''
Main
'''

#Get command line args
parser = argparse.ArgumentParser(description='Produce simple u,v drift time correlation with resolution')
parser.add_argument('--res', action='store', dest='resolution' , type=float , default=-1., required=True, help='Set straw resolution in microns')
parser.add_argument('--nev', action='store', dest='nevents' , type=int , default=-1, required=True, help='Num hits to generate')
parser.add_argument('--draw', action='store_true', dest='drawEvents')
parser.add_argument('--verbose', action='store_true', dest='verbose')
args = parser.parse_args()

#Define geom
strawAngle = 7.5 #deg
strawGradient = 1. / math.tan( math.radians(strawAngle) )
strawMinZ = -42.6321e3
strawMaxZ = 42.6321e3

#Generate events
residuals = []
smearingVals = []
interceptSmearingVals = []
doubletSmearedIsochroneLineResiduals = []
for i in xrange(0,args.nevents,1):    

  if args.verbose: print '\nEvent',i

  if args.drawEvents: plt.title('Event %i : Truth vs reco hits (shows result of single straw resolution)' % (i) )

  #Get hit pos (transverse)
  truthHitPos = Coord( y=gauss(0.,3.e3) , z=gauss(0.,3.e3) )
  if args.verbose: print "Truth hit pos =",truthHitPos
  if args.drawEvents: plt.scatter([truthHitPos.y],[truthHitPos.z],marker='o',c='blue')

  #Get truth ioschrone lines for each doublet from hit pos
  doubletTruthIsochroneLines = []
  for i_d in range(0,2) : #Loop over doublets
    gradientSign = -1. if i_d % 2 == 0 else 1.  #One view is +ve, other -ve
    m = gradientSign * strawGradient
    truthIsochroneLine = Line( m=m , c=truthHitPos.z-(m*truthHitPos.y) )
    if args.verbose: print "Truth isochrone line =",truthIsochroneLine
    doubletTruthIsochroneLines.append( truthIsochroneLine )
    if args.drawEvents: #Draw it
      lineYVals,lineZVals = getLineEndsFromZ(strawMinZ,strawMaxZ,truthIsochroneLine)
      plt.plot(lineYVals,lineZVals,"b--")

  #The intercept of a indivudual straw isochroine line (really cylinder) changes 
  #according to the resolution (which affects radial measurements)
  #Make this change and see effect
  doubletSmearedIsochroneLines = []
  for truthIsochroneLine in doubletTruthIsochroneLines :

    #Smear intercept in both straws and get mean (reco takes mean)
    interceptSum = 0.
    for i_s in range(0,2) :
      smearing = gauss(0.,args.resolution)
      if args.verbose: print "Smearing (single straw) =",smearing
      smearingVals.append(smearing)
      smearedIntercept = truthIsochroneLine.c + (truthIsochroneLine.m*smearing) #Smear intercept
      smearedInterceptResidual = smearedIntercept - truthIsochroneLine.c
      if args.verbose: print "Smearing (doublet ioschrone line) =",smearedInterceptResidual
      interceptSmearingVals.append( smearedInterceptResidual ) #Record residuals
      interceptSum += smearedIntercept
    interceptMean = interceptSum / 2.

    #Record as new ioschrone
    smearedDoubletIsochroneLine = Line( m=truthIsochroneLine.m , c=interceptMean )
    if args.verbose: print "Smeared isochrone line =",smearedDoubletIsochroneLine
    doubletSmearedIsochroneLines.append( smearedDoubletIsochroneLine )    

    #Record residual of new mean doublet isochrone line to truth
    lineYVals,lineZVals = getLineEndsFromZ(strawMinZ,strawMaxZ,smearedDoubletIsochroneLine)
    doubletSmearedIsochroneLineResiduals.append( dca( [lineYVals[0],lineZVals[0]] , [lineYVals[1],lineZVals[1]] , [truthHitPos.y,truthHitPos.z] ) )

    #Draw it
    if args.drawEvents: plt.plot(lineYVals,lineZVals,"r--")


  #Find new hit position from smeared lines
  #  y = (c_v - c_u) / (m_u - m_v)   
  #  z = m_u * y + c_u   (double use either view m and c)
  yReco = ( doubletSmearedIsochroneLines[0].c - doubletSmearedIsochroneLines[1].c ) / ( doubletSmearedIsochroneLines[1].m - doubletSmearedIsochroneLines[0].m )
  zReco = ( doubletSmearedIsochroneLines[0].m * yReco ) + doubletSmearedIsochroneLines[0].c
  recoHitPos = Coord( y=yReco , z=zReco )
  if args.verbose: print "Reco hit pos =",recoHitPos
  if args.drawEvents: plt.scatter([recoHitPos.y],[recoHitPos.z],marker='o',c='red')

  #Show isochrone lines and hit positons on a plot
  if args.drawEvents: plt.show()

  #Get residuals
  residual = Coord( y=recoHitPos.y-truthHitPos.y , z=recoHitPos.z-truthHitPos.z )
  if args.verbose: print "Residual =",residual
  residuals.append(residual)

#Create grid to add plots to
figure, grid = plt.subplots(2,2)
plt.suptitle('Straw resolution effect on hit reconstruction : Resolution = %f um' % (args.resolution) , fontsize=20)

#Plot the single straw smearing
n,bins,patches = grid[0][0].hist(np.array(smearingVals),bins=100,normed=True) #Fill hist (normalise for Gaussian fitting)
(mu, sigma) = norm.fit(smearingVals) #Fit Gaussian
grid[0][0].plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2) #Plot the fit
grid[0][0].set_title('Single straw smearing [um]\nmean=%f : sigma=%f'%(mu,sigma))
#grid[0][0].set_xlabel('[um]',horizontalalignment='left')

#Plot the doublet isochrone (mean of two straws) residuals
n,bins,patches = grid[0][1].hist(np.array(doubletSmearedIsochroneLineResiduals),bins=100,normed=True) #Fill hist (normalise for Gaussian fitting)
(mu, sigma) = norm.fit(doubletSmearedIsochroneLineResiduals) #Fit Gaussian
grid[0][1].plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2) #Plot the fit
grid[0][1].set_title('Doublet mean isochrone residuals [um]\nmean=%f : sigma=%f'%(mu,sigma))
#grid[0][1].set_xlabel('[um]')

#Plot the y residuals (with Gaussian fit)
yResiduals = []  #Get list of y residuals
for res in residuals : yResiduals.append(res.y)
n,bins,patches = grid[1][0].hist(np.array(yResiduals),bins=100,normed=True) #Fill hist (normalise for Gaussian fitting)
(mu, sigma) = norm.fit(yResiduals) #Fit Gaussian
grid[1][0].plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2) #Plot the fit
grid[1][0].set_title('Fit y residuals [um]\nmean=%f : sigma=%f'%(mu,sigma))
#grid[1][0].set_xlabel('[um]')

#Plot the z residuals (with Gaussian fit)
zResidualsUm = []  #Get list of z residuals
for res in residuals : zResidualsUm.append(res.z)
n,bins,patches = grid[1][1].hist(np.array(zResidualsUm),bins=100,normed=True) #Fill hist (normalise for Gaussian fitting)
(mu, sigma) = norm.fit(zResidualsUm) #Fit Gaussian
grid[1][1].plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2) #Plot the fit
grid[1][1].set_title('Fit z residuals [um]\nmean=%f : sigma=%f'%(mu,sigma))
#grid[1][1].set_xlabel('[um]')

#Draw plot grid
plt.show()

