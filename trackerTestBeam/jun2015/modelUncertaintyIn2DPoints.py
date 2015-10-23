#This script demonstrates that for a distribution of 2D points with independent errors, 68% of events fall within a an ellipse with axes of 1.515*sigma, not 1 sigma. E.g. this is how to correctly combine the errors.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.patches import Ellipse
from scipy.optimize import curve_fit
from scipy.stats import chi2
from sys import argv,exit
import datetime
from math import log10,pow,sqrt,fabs
from random import gauss,uniform
import argparse


#
# Main
#

parser = argparse.ArgumentParser(description='Produce simple u,v drift time correlation with resolution')
parser.add_argument('--sigmaX', action='store', dest='sigmaX' , type=float , required=True)
parser.add_argument('--sigmaY', action='store', dest='sigmaY' , type=float , required=True)
parser.add_argument('--nev', action='store', dest='nevents' , type=int , required=True)
args = parser.parse_args()

if args.nevents < 1 :
  print "ERROR: Number of events < 1"
  exit(-1)

smearedXVals = []
smearedYVals = []
residualXVals = []
residualYVals = []
residualDCAVals = []

ellipseScaleFactor = 1.515

# Generate points
numInSigmaElipse = 0
numInScaledSigmaElipse = 0
for i in range(0,args.nevents):    

  truthX = 0.
  truthY = 0.

  smearedX = gauss(truthX,args.sigmaX)
  smearedXVals.append(smearedX)
  smearedY = gauss(truthY,args.sigmaY)
  smearedYVals.append(smearedY)

  residualX = smearedX - truthX
  residualXVals.append(residualX)
  residualY = smearedY - truthY
  residualYVals.append(residualY)

  residualDCA = sqrt( residualX**2. + residualY**2. )
  residualDCAVals.append( residualDCA )

  #Check if point falls within 1 sigma ellipse
  if (smearedX**2./args.sigmaX**2) + (smearedY**2./args.sigmaY**2) < 1. :
    numInSigmaElipse += 1

  #Check if point falls within scaled sigma ellipse

  if (smearedX**2./(args.sigmaX*ellipseScaleFactor)**2) + (smearedY**2./(args.sigmaY*ellipseScaleFactor)**2) < 1. :
    numInScaledSigmaElipse += 1

print "Fraction of points in 1 sigma ellipse = %f" % ( float(numInSigmaElipse)/float(args.nevents) )
print "Fraction of points in %f sigma ellipse = %f" % ( ellipseScaleFactor, float(numInScaledSigmaElipse)/float(args.nevents) )

#Plot the smeared positions
plt.title('Smeared positions')
plt.scatter(np.array(smearedXVals),np.array(residualYVals),marker='.',c='blue')
plt.show()

#Plot the residuals
plt.title('Residuals')
plt.scatter(np.array(residualXVals),np.array(residualYVals),marker='.',c='blue')
plt.show()


