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


#
# Main
#

firstProtonXVals = []
firstProtonYVals = []
secondProtonXVals = []
secondProtonYVals = []

doubleOccXDiff = []
doubleOccYDiff = []

beamXVals = []
beamYVals = []

# Generate tracks
numEvents = 10000
beamXRMS = 3.
beamYRMS = 3.
doubleOccProbability = 0.35
for i in xrange(0,numEvents,1):    

  #Generate proton transverse position
  x = gauss(0.,beamXRMS)
  y = gauss(0.,beamYRMS)
  firstProtonXVals.append(x)
  firstProtonYVals.append(y)

  #Generate another proton if double occupancy event
  if uniform(0.,1.) < doubleOccProbability :

    #Generate proton transverse position
    x = gauss(0.,beamXRMS)
    y = gauss(0.,beamYRMS)
    secondProtonXVals.append(x)
    secondProtonYVals.append(y)

    #Record distance between the two protons in same bucket
    doubleOccXDiff.append( secondProtonXVals[-1] - firstProtonXVals[-1]  )
    doubleOccYDiff.append( secondProtonYVals[-1] - firstProtonYVals[-1]  )

#Plot hits
plt.title('Beam transverse (cross-section) positions [mm]')
plt.scatter(np.array(firstProtonXVals),np.array(firstProtonYVals),marker='.',c='blue')
plt.scatter(np.array(secondProtonXVals),np.array(secondProtonYVals),marker='.',c='red')
plt.show()

#Plot displacement between hits in same bucket
plt.title('Displacement between protons from same bucket [mm]')
plt.scatter(np.array(doubleOccXDiff),np.array(doubleOccYDiff),marker='.',c='blue')
plt.show()

#Plot x vs x diff
plt.title('x vs x diff [mm]')
plt.scatter(np.array(secondProtonXVals),np.array(doubleOccXDiff),marker='.',c='blue')
plt.show()

#Plot y vs y diff
plt.title('y vs y diff [mm]')
plt.scatter(np.array(secondProtonYVals),np.array(doubleOccYDiff),marker='.',c='blue')
plt.show()

