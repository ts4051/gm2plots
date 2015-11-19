#This script just shows how error improves when taking multiple measurements and averaging
#Straws in same view basically do this, e.g. take mean of two measurements of same isochrone line (as well as disambiguating)

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

measurementSigma = 1.
numMeasurements = 2

meanMeasurementVals = []

numEvents = 10000
for i_e in range(0,numEvents) :

  measuredVals = []
  for i_m in range(0,numMeasurements) :

    truth = 0.
    measured = gauss(truth,measurementSigma)
    measuredVals.append(measured)

  meanMeasurement = sum(measuredVals) / float(len(measuredVals))
  meanMeasurementVals.append(meanMeasurement)

print "Measurement sigma (truth) = %f" % (measurementSigma)
print "Expected sigma improvement for %i measurements = %f" % (numMeasurements,measurementSigma/np.sqrt(numMeasurements))

n,bins,patches = plt.hist(np.array(meanMeasurementVals),bins=100,normed=True) #Fill hist (normalise for Gaussian fitting)
(mu, sigma) = norm.fit(meanMeasurementVals) #Fit Gaussian
print "Mean of measurements : Mean = %f : Sigma = %f" % (mu,sigma) 
plt.plot(bins, mlab.normpdf(bins,mu,sigma), 'r--', linewidth=2) #Plot the fit
plt.show()

