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


def uniformSmear(val,smear) :
  smearedVal = uniform(val-(smear/2.),val+(smear/2.))
  #print "Uniform smear: Input value = %f, smeared value = %f, smear = %f" % (val,smearedVal,smear)
  return smearedVal


def gaussSmear(val,smear) :
  smearedVal = gauss(val,smear)
  #print "Gaussian smear: Input value = %f, smeared value = %f, smear = %f" % (val,smearedVal,smear)
  return smearedVal


def fixTime(time):
    #if (time < 0): #TODO Do we want this?
    #    time = fabs(time)
    return time


def straight_line_fit(z, a, b):
  return a + b*z


def gaussian_fit(x,A,mu,sigma):
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))


#
# Main
#

parser = argparse.ArgumentParser(description='Produce simple u,v drift time correlation with resolution')
parser.add_argument('--res', action='store', dest='resolution' , type=float , default = -1., help='Set straw resolution in microns')
parser.add_argument('--nev', action='store', dest='nevents' , type=int , default = -1, help='Num hits to generate')
parser.add_argument('--bg', action='store', dest='bgfrac' , type=float , default = -1., help='Signal / background fraction')
parser.add_argument('--sumcut', action='store', dest='sumcut' , type=float , default = -1., help='Drift time sum cut')
args = parser.parse_args()

# Straw radius [um]
strawRadius = 2500.
# Drift velocity: 50 microns per ns (is this true for ethane ?)
driftVelocity = 50
# Maxium drift time (from drift velocity and radius)
driftTimeMax = strawRadius / driftVelocity

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
thit = resol/driftVelocity
print 'Time resolution (from distance resolution) [ns] =',thit

#Smear to compensate for fine time binning issue (uniform smear)
#finetime_smear = 0. #ns
finetime_smear = 2.5 #ns
print 'Fine time binning smearing [ns] =',finetime_smear

#Smear to compensate for uncertainty in silicon-straws time sync (gaussian smear)
timesync_smear = 0. #ns
#timesync_smear = 2.5 #ns
print 'Silicon/straw time sync smearing [ns] =',timesync_smear


driftTimeL0Vals = []
driftTimeL1Vals = []
driftTimeL0ValsCut = []
driftTimeL1ValsCut = []
singleStrawDriftDistResidualVals = []
singleStrawDriftTimeResidualVals = []

# Generate hit pairs
for i in xrange(0,nev,1):    

  #Layer 0
  hitPosL0 = uniform(0.,strawRadius) #Generate hit DCA
  hitPosL0Smeared = gaussSmear(hitPosL0,resol) #Smear for resolution
  singleStrawDriftDistResidualVals.append(hitPosL0Smeared-hitPosL0) 
  driftTimeL0 = hitPosL0Smeared / driftVelocity #Convert to time
  driftTimeL0 = fixTime( uniformSmear(driftTimeL0,finetime_smear) ) #Fine time binning smear
  driftTimeL0 = fixTime(gaussSmear(driftTimeL0, timesync_smear)) #Time sync smear
  singleStrawDriftTimeResidualVals.append(driftTimeL0-(hitPosL0/driftVelocity)) 

  #Layer 1
  hitPosL1 = strawRadius - hitPosL0 #Anticorrelated hit DCA
  hitPosL1Smeared = gaussSmear(hitPosL1,resol) #Smear for resolution
  singleStrawDriftDistResidualVals.append(hitPosL1Smeared-hitPosL1) 
  driftTimeL1 = hitPosL1Smeared / driftVelocity #Convert to time
  driftTimeL1 = fixTime( uniformSmear(driftTimeL1,finetime_smear) ) #Fine time binning smear
  driftTimeL1 = fixTime(gaussSmear(driftTimeL1, timesync_smear)) #Time sync smear
  singleStrawDriftTimeResidualVals.append(driftTimeL1-(hitPosL1/driftVelocity)) 

  #Only record hit if passes sum cut
  driftTimeSum = driftTimeL0 + driftTimeL1
  if (driftTimeMax-sumcut) <= driftTimeSum <= (driftTimeMax+sumcut) : 
    driftTimeL0Vals.append(driftTimeL0)
    driftTimeL1Vals.append(driftTimeL1)
    #print (driftTimeL0,driftTimeL1)
  else:
    driftTimeL0ValsCut.append(driftTimeL0) #Record cut hit positions too
    driftTimeL1ValsCut.append(driftTimeL1)


# Generate uncorrelated background
for i in xrange(0,int(nev*bgfrac),1):  
  
  #Layer 0
  hitPosL0 = uniform(0.,strawRadius)
  hitPosL0Smeared = gaussSmear(hitPosL0,resol) #Smear for resolution
  driftTimeL0 = hitPosL0Smeared / driftVelocity #Convert to time
  driftTimeL0 = fixTime( uniformSmear(driftTimeL0,finetime_smear) ) #Fine time binning smear
  driftTimeL0 = fixTime( gaussSmear(driftTimeL0, timesync_smear)) #Time sync smear

  #Layer 1
  hitPosL1 = uniform(0.,strawRadius) #Uncorrelated
  hitPosL1Smeared = gaussSmear(hitPosL1,resol) #Smear for resolution
  driftTimeL1 = hitPosL1Smeared / driftVelocity #Convert to time
  driftTimeL1 = fixTime( uniformSmear(driftTimeL1,finetime_smear) ) #Fine time binning smear
  driftTimeL1 = fixTime(gaussSmear(driftTimeL1, timesync_smear)) #Time sync smear

  #Only record hit if passes sum cut
  driftTimeSum = driftTimeL0 + driftTimeL1
  if (driftTimeMax-sumcut) <= driftTimeSum <= (driftTimeMax+sumcut) : 
    driftTimeL0Vals.append(driftTimeL0)
    driftTimeL1Vals.append(driftTimeL1)
    #print (driftTimeL0,driftTimeL1)
  else:
    driftTimeL0ValsCut.append(driftTimeL0) #Record cut hit positions too
    driftTimeL1ValsCut.append(driftTimeL1)

if len(driftTimeL0Vals)==0 :
  print 'No data passed cuts'
  exit(0)

x = np.array(driftTimeL0Vals)  
y = np.array(driftTimeL1Vals)  
xcut = np.array(driftTimeL0ValsCut)  
ycut = np.array(driftTimeL1ValsCut)  

# Fit these to a straight line
popt, pcov = curve_fit(straight_line_fit, x, y)
fitGradient = popt[1]
fitIntercept = popt[0]
print "Fit: gradient = %f, intercept = %f" % (fitGradient,fitIntercept)

# Best fit line end points
xFit = [-10.,driftTimeMax+10.]
yFit = [ fitGradient*xFit[0]+fitIntercept , fitGradient*xFit[1]+fitIntercept ]

#Plot drift times
plt.title('Drift times in doublet (layer0=x,layer1=y) [ns]')
plt.scatter(x,y,marker='.',c='blue')
plt.plot(xFit,yFit,"g-")
plt.show()

#Also plot with cut hits
plt.title('Drift times in doublet (layer0=x,layer1=y) [ns]')
plt.scatter(x,y,marker='o',c='blue')
plt.scatter(xcut,ycut,marker='o',c='red')
plt.plot(xFit,yFit,"g-")
plt.show()

#Plot distance residuals
mean = np.mean(singleStrawDriftDistResidualVals)
variance = np.var(singleStrawDriftDistResidualVals)
sigma = np.sqrt(variance)
print "Mean = %f um , Sigma = %f um" % (mean,sigma)
plt.title('Single straw drift distance residuals [um] (normalised)')
plt.hist(singleStrawDriftDistResidualVals, normed=True, bins=100)
plt.show()

#Plot time residuals
mean = np.mean(singleStrawDriftTimeResidualVals)
variance = np.var(singleStrawDriftTimeResidualVals)
sigma = np.sqrt(variance)
print "Mean = %f ns , Sigma = %f ns" % (mean,sigma)
plt.title('Single straw drift time residuals [ns] (normalised)')
plt.hist(singleStrawDriftTimeResidualVals, normed=True, bins=100)
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
print "Residuals Gaussian: mean = %f, sigma = %f [ns]" % (mean,sigma) 
numBins = 100
x = np.linspace(min(RPTS), max(RPTS),numBins) #Bins
plt.title('Time residuals [ns] (normalised)')
plt.hist(RPTS, bins=numBins,normed=True) #Must normalise histogram for Gaussian overlay
plt.plot(x,mlab.normpdf(x,mean,sigma),"r") #Plot bins
plt.show()

#Plot sum of drift times
driftTimeSumVals = list()
for i in range(0,len(driftTimeL0Vals)) : driftTimeSumVals.append( driftTimeL0Vals[i] + driftTimeL1Vals[i] )
mean = np.mean(driftTimeSumVals)
variance = np.var(driftTimeSumVals)
sigma = np.sqrt(variance)
print "Drift time sum residuals: mean = %f, sigma = %f, single straw sigma = %f [ns]" % (mean,sigma,sigma/np.sqrt(2.)) 
numBins = 100
x = np.linspace(min(driftTimeSumVals), max(driftTimeSumVals),numBins) #Bins
plt.title('Drift time sum residuals [ns] (normalised)')
plt.hist(driftTimeSumVals, bins=numBins,normed=True) #Must normalise histogram for Gaussian overlay
plt.plot(x,mlab.normpdf(x,mean,sigma),"r") #Plot bins
plt.show()


