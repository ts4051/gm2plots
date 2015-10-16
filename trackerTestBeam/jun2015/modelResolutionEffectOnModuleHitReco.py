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


'''
Main
'''

#Get command line args
parser = argparse.ArgumentParser(description='Produce simple u,v drift time correlation with resolution')
parser.add_argument('--res', action='store', dest='resolution' , type=float , default=-1., required=True, help='Set straw resolution in microns')
parser.add_argument('--nev', action='store', dest='nevents' , type=int , default=-1, required=True, help='Num hits to generate')
parser.add_argument('--plot', action='store_true', dest='plot')
parser.add_argument('--verbose', action='store_true', dest='verbose')
args = parser.parse_args()

# Drift velocity: 50 microns per ns (is this true for ethane ?)
driftVelocity = 50

# Resolution, smearing to add to hit time due to resolution    
#timeResolution = args.resolution/driftVelocity
#print 'Time resolution (from distance resolution) [ns] =',timeResolution

#finetime_smear = 0. #ns
#finetime_smear = 2.5 #ns
#print 'Fine time binning smearing [ns] =',finetime_smear

#Define geom
strawAngle = 7.5 #deg
strawGradient = 1. / math.tan( math.radians(strawAngle) )
strawMinZ = -42.6321e3
strawMaxZ = 42.6321e3



#Generate events
residuals = []
smearingVals = []
interceptSmearingVals = []
for i in xrange(0,args.nevents,1):    

  if args.verbose: print '\nEvent',i

  if args.plot: plt.title('Event %i : Truth vs reco hits (shows result of single straw resolution)' % (i) )

  #Get hit pos (transverse)
  truthHitPos = Coord( y=gauss(0.,3.e3) , z=gauss(0.,3.e3) )
  if args.verbose: print "Truth hit pos =",truthHitPos
  if args.plot: plt.scatter([truthHitPos.y],[truthHitPos.z],marker='o',c='blue')

  #Get truth ioschrone lines for each doublet from hit pos
  doubletTruthIsochroneLines = []
  for i_d in range(0,2) : #Loop over doublets
    gradientSign = -1. if i_d % 2 == 0 else 1.  #One view is +ve, other -ve
    m = gradientSign * strawGradient
    truthIsochroneLine = Line( m=m , c=truthHitPos.z-(m*truthHitPos.y) )
    if args.verbose: print "Truth isochrone line =",truthIsochroneLine
    doubletTruthIsochroneLines.append( truthIsochroneLine )
    if args.plot: #Draw it
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
    smearedIsochroneLine = Line( m=truthIsochroneLine.m , c=interceptMean )
    if args.verbose: print "Smeared isochrone line =",smearedIsochroneLine
    doubletSmearedIsochroneLines.append( smearedIsochroneLine )
    if args.plot: #Draw it
      lineYVals,lineZVals = getLineEndsFromZ(strawMinZ,strawMaxZ,smearedIsochroneLine)
      plt.plot(lineYVals,lineZVals,"r--")

  #Find new hit position from smeared lines
  #  y = (c_v - c_u) / (m_u - m_v)   
  #  z = m_u * y + c_u   (double use either view m and c)
  yReco = ( doubletSmearedIsochroneLines[0].c - doubletSmearedIsochroneLines[1].c ) / ( doubletSmearedIsochroneLines[1].m - doubletSmearedIsochroneLines[0].m )
  zReco = ( doubletSmearedIsochroneLines[0].m * yReco ) + doubletSmearedIsochroneLines[0].c
  recoHitPos = Coord( y=yReco , z=zReco )
  if args.verbose: print "Reco hit pos =",recoHitPos
  if args.plot: plt.scatter([recoHitPos.y],[recoHitPos.z],marker='o',c='red')

  #Show isochrone lines and hit positons on a plot
  if args.plot: plt.show()

  #Get residuals
  residual = Coord( y=recoHitPos.y-truthHitPos.y , z=recoHitPos.z-truthHitPos.z )
  if args.verbose: print "Residual =",residual
  residuals.append(residual)

#Plot the single straw smearing
n,bins,patches = plt.hist(np.array(smearingVals),bins=100,normed=True) #Fill hist (normalise for Gaussian fitting)
(mu, sigma) = norm.fit(smearingVals) #Fit Gaussian
plt.plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2) #Plot the fit
plt.title('Single straw smearing : mean=%f sigma=%f : [um]'%(mu,sigma))
plt.show()

#Plot the intercept smearing
n,bins,patches = plt.hist(np.array(interceptSmearingVals),bins=100,normed=True) #Fill hist (normalise for Gaussian fitting)
(mu, sigma) = norm.fit(interceptSmearingVals) #Fit Gaussian
plt.plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2) #Plot the fit
plt.title('Intercept smearing : mean=%f sigma=%f : [um]'%(mu,sigma))
plt.show()

#Plot the y residuals (with Gaussian fit)
yResiduals = []  #Get list of y residuals
for res in residuals : yResiduals.append(res.y)
n,bins,patches = plt.hist(np.array(yResiduals),bins=100,normed=True) #Fill hist (normalise for Gaussian fitting)
(mu, sigma) = norm.fit(yResiduals) #Fit Gaussian
plt.plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2) #Plot the fit
plt.title('Fit y residuals : mean=%f sigma=%f : [um]'%(mu,sigma))
plt.show()

#Plot the z residuals (with Gaussian fit)
zResidualsUm = []  #Get list of z residuals
for res in residuals : zResidualsUm.append(res.z)
n,bins,patches = plt.hist(np.array(zResidualsUm),bins=100,normed=True) #Fill hist (normalise for Gaussian fitting)
(mu, sigma) = norm.fit(zResidualsUm) #Fit Gaussian
plt.plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2) #Plot the fit
plt.title('Fit z residuals : mean=%f sigma=%f : [um]'%(mu,sigma))
plt.show()

