import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.optimize import curve_fit
from scipy.stats import chi2
from sys import argv,exit
import datetime
from math import log10,pow,sqrt,fabs
from random import gauss,uniform
from ml.root import histom
import argparse

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

def fixTime(time):
    if (time < 0):
        time = fabs(time)
    return time

def straight_line_fit(z, a, b):
  return a + b*z

parser = argparse.ArgumentParser(description='Produce simple u,v drift time correlation with resolution')
parser.add_argument('--res', action='store', dest='resolution' , default = -1, help='Set straw resolution in microns')
parser.add_argument('--nev', action='store', dest='nevents' , default = -1, help='Num hits to generate')
args = parser.parse_args()

# Drift velocity: 50 microns per ns (is this true for ethane ?)
TD = 50
# Maxium drift time : 50 ns
MAXD = 50

if (args.resolution == -1):
    print "\nERROR: --res must be set\n\n"
    parser.print_help()
    exit (-1)
else:
    resol = int(args.resolution)

if (args.nevents == -1):
    print "\nERROR: --nev must be set\n\n"
    parser.print_help()
    exit (-1)
else:
    nev = int(args.nevents)

# Resolution, smearing to add to hit time due to resolution    
thit = resol/TD

hitu_smear = []
hitv_smear = []

# Generate hit pairs
for i in xrange(0,nev,1):    
  hitu = uniform(0.0, 50.0)
  uhit = fixTime(gauss(hitu, thit)) 
  hitu_smear.append(uhit)
  hitv = MAXD - hitu
  vhit = fixTime(gauss(hitv, thit)) 
  hitv_smear.append (vhit)

x = np.array(hitu_smear)  
y = np.array(hitv_smear)  

# Fit these to a straight line
popt, pcov = curve_fit(straight_line_fit, x, y)
print "Fit: gradient = %f, intercept = %f \n" % (popt[1], popt[0])

#plt.scatter(x,y,marker='o',c='blue')
#plt.show()

# Loop over the hits and plot the residual (dca)
residuals = []

# Best fit line defined by these two points
start = [-50,100]
end  = [100,-50]

for i in xrange(0,len(x)):
    xv = x[i]
    yv = y[i]
    point = [xv,yv]

    try:
# Residual from DCA        
#      resid = dca(start,end,point)

# Residual a la Tom
# Predicted y
      yp = popt[0] + xv*popt[1]
      resid = yv - yp 
      residuals.append(resid)
    except ValueError as err:
      print(err.args)
    
RPTS = np.array(residuals)
mean = np.mean(RPTS)
variance = np.var(RPTS)
sigma = np.sqrt(variance)
x = np.linspace(min(RPTS), max(RPTS),100)
#plt.hist(RPTS)
#plt.plot(x,mlab.normpdf(x,mean,sigma))
#plt.show()
print "Residuals Mean = %f, Sigma = %f" % (mean,sigma)
#



