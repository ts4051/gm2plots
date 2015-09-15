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

def gaussian_fit(x,A,mu,sigma):
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

parser = argparse.ArgumentParser(description='Produce simple u,v drift time correlation with resolution')
parser.add_argument('--res', action='store', dest='resolution' , type=float , default = -1., help='Set straw resolution in microns')
parser.add_argument('--nev', action='store', dest='nevents' , type=int , default = -1, help='Num hits to generate')
parser.add_argument('--bg', action='store', dest='bgfrac' , type=float , default = -1., help='Signal / background fraction')
parser.add_argument('--sumcut', action='store', dest='sumcut' , type=float , default = -1., help='Drift time sum cut')
args = parser.parse_args()

# Drift velocity: 50 microns per ns (is this true for ethane ?)
VD = 50
# Maxium drift time : 50 ns
MAXD = 50

if (args.resolution == -1):
    print "\nERROR: --res must be set\n\n"
    parser.print_help()
    exit (-1)
else:
    resol = int(args.resolution)
    print 'Distance resolution [um] =',resol

if (args.nevents == -1):
    print "\nERROR: --nev must be set\n\n"
    parser.print_help()
    exit (-1)
else:
    nev = int(args.nevents)

if (args.bgfrac == -1.):
    print "\nERROR: --bg must be set\n\n"
    parser.print_help()
    exit (-1)
elif args.bgfrac<0. or args.bgfrac>1. :
    print "\nERROR: --bg must be in range [0.,1.]\n\n"
    exit (-1)
else:
    bgfrac = args.bgfrac
    print 'Signal / background fraction =',bgfrac

if (args.sumcut == -1):
    print "\nERROR: --sumcut must be set\n\n"
    parser.print_help()
    exit (-1)
else:
    sumcut = int(args.sumcut)

# Resolution, smearing to add to hit time due to resolution    
thit = resol/VD
print 'Time resolution (from distance resolution) [ns] =',thit

#finetime_smear = 0. #ns
finetime_smear = 2.5 #ns
print 'Fine time binning smearing [ns] =',finetime_smear

#timesync_smear = 0. #ns
timesync_smear = 2.5 #ns
print 'Silicon/straw time sync smearing [ns] =',timesync_smear

hitu_smear = []
hitv_smear = []

# Generate hit pairs
for i in xrange(0,nev,1):    

  hitu = uniform(0.0, 50.0)
  uhit = fixTime(gauss(hitu, thit)) #Resolution smear
  uhit = fixTime(gauss(uhit, finetime_smear)) #Fine time binning smear
  uhit = fixTime(gauss(uhit, timesync_smear)) #Time sync smear

  hitv = MAXD - hitu
  vhit = fixTime(gauss(hitv, thit)) #Resolution smear
  vhit = fixTime(gauss(vhit, finetime_smear)) #Fine time binning smear
  vhit = fixTime(gauss(vhit, timesync_smear)) #Time sync smear

  #Only record hit if passes sum cut
  if (MAXD-sumcut) <= (uhit+vhit) <= (MAXD+sumcut) : 
    hitu_smear.append(uhit)
    hitv_smear.append(vhit)
    #print (uhit,hitv)

# Generate uncorrelated background
for i in xrange(0,int(nev*bgfrac),1):  
  
  hitu = uniform(0.0, 50.0)
  uhit = fixTime(gauss(hitu, finetime_smear)) #Fine time binning smear
  uhit = fixTime(gauss(uhit, timesync_smear)) #Time sync smear

  hitv = uniform(0.0, 50.0) #Uncorrelated
  vhit = fixTime(gauss(hitv, finetime_smear)) #Fine time binning smear
  vhit = fixTime(gauss(vhit, timesync_smear)) #Time sync smear

  #Only record hit if passes sum cut
  if (MAXD-sumcut) <= (uhit+vhit) <= (MAXD+sumcut) : 
    hitu_smear.append(uhit)
    hitv_smear.append(vhit)
    #print (uhit,hitv)

if len(hitu_smear)==0 :
  print 'No data passed cuts'
  exit(0)

x = np.array(hitu_smear)  
y = np.array(hitv_smear)  

# Fit these to a straight line
popt, pcov = curve_fit(straight_line_fit, x, y)
fitGradient = popt[1]
fitIntercept = popt[0]
print "Fit: gradient = %f, intercept = %f" % (fitGradient,fitIntercept)

# Best fit line end points
xFit = [-20.,70.]
yFit = [ fitGradient*xFit[0]+fitIntercept , fitGradient*xFit[1]+fitIntercept ]

#Plot
plt.title('Drift times in doublet (layer0=x,layer1=y) [ns]')
plt.scatter(x,y,marker='.',c='blue')
plt.plot([xFit[0],yFit[0]],[xFit[1],yFit[1]],"r--")
plt.show()

# Loop over the hits and plot the residual (dca)
residuals = []

for i in xrange(0,len(x)):
    xv = x[i]
    yv = y[i]
    point = [xv,yv]

    try:
# Residual from DCA        
      resid = dca((xFit[0],yFit[0]),(xFit[1],yFit[1]),point)
      residuals.append(resid)
    except ValueError as err:
      print(err.args)
    
#Plot the residuals
RPTS = np.array(residuals) #Residuals
mean = np.mean(RPTS)
variance = np.var(RPTS)
sigma = np.sqrt(variance)
print "Residuals Gaussian: mean = %f, variance = %f, sigma = %f" % (mean,variance,sigma) 
x = np.linspace(min(RPTS), max(RPTS),100) #Bins
plt.title('Time residuals [ns] (normalised)')
plt.hist(RPTS, normed=True) #Must normalise histogram for Gaussian overlay
plt.plot(x,mlab.normpdf(x,mean,sigma),"r") #Plot bins
plt.show()
print "Residuals Mean = %f, Sigma = %f" % (mean,sigma)
#

