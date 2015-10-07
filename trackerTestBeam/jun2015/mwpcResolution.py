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


#
# Main
#

beamXVals = []
beamYVals = []

# Generate tracks
numEvents = 10000
beamXRMS = 3.
beamYRMS = 3.
for i in xrange(0,numEvents,1):    

  #Generate beam start point
  x = gauss(0.,beamXRMS)
  y = gauss(0.,beamYRMS)

  #Record for plotting
  beamXVals.append(x)
  beamYVals.append(y)

#Convert lists to np arrays
xBeam = np.array(beamXVals)  
yBeam = np.array(beamYVals)

#Plot
plt.title('Beam transverse (cross-section) positions [mm]')
plt.scatter(xBeam,yBeam,marker='.',c='blue')
plt.show()


