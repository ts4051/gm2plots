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


#Helper functions
def getLineY(x,m,c):
  return m*x + c

def getLineX(y,m,c):
  return (y-c)/m

def getLineEndsFromY(m,c,y1,y2):
  yVals = [y1,y2]
  xVals = [ getLineX(yVals[0],m,c) , getLineX(yVals[1],m,c) ]
  return xVals,yVals


#Init plot
plt.title('Hit reco')


#Define straw wires (from top/bottom point coords)
wireU0X = [-7.44632,-18.6716] #bottom,top
wireU0Y = [-42.6321,42.6321]
wireU1X = [-4.41632,-15.6416]
wireU1Y = [-42.6321,42.6321]
plt.plot(wireU0X,wireU0Y,"r-")
plt.plot(wireU1X,wireU1Y,"r-")

wireV0X = [-21.7737,-10.5484]
wireV0Y = [-42.6321,42.6321]
wireV1X = [-18.8037,-7.57843]
wireV1Y = [-42.6321,42.6321]
plt.plot(wireV0X,wireV0Y,"b-")
plt.plot(wireV1X,wireV1Y,"b-")


#Define straw isochrone lines (from gradient/intecepts)


#Define straw corrected isochrone lines (from gradient/intecepts)
wireCorrIsoU0X,wireCorrIsoU0Y = getLineEndsFromY(-7.59575,-86.1444,-42.6321,42.6321)
plt.plot(wireCorrIsoU0X,wireCorrIsoU0Y,"r--")
wireCorrIsoU1X,wireCorrIsoU1Y = getLineEndsFromY(-7.59575,-84.0446,-42.6321,42.6321)
plt.plot(wireCorrIsoU1X,wireCorrIsoU1Y,"r--")

wireCorrIsoV0X,wireCorrIsoV0Y = getLineEndsFromY(7.59575,115.319,-42.6321,42.6321)
plt.plot(wireCorrIsoV0X,wireCorrIsoV0Y,"b--")
wireCorrIsoV1X,wireCorrIsoV1Y = getLineEndsFromY(7.59575,113.675,-42.6321,42.6321)
plt.plot(wireCorrIsoV1X,wireCorrIsoV1Y,"b--")


#Define doublet isochrone overlap lines (from gradient/intecepts)
doubletIsoUX,doubletIsoUY = getLineEndsFromY(-7.59575,-85.0945,-42.6321,42.6321)
plt.plot(doubletIsoUX,doubletIsoUY,"r:")

doubletIsoVX,doubletIsoVY = getLineEndsFromY(7.59575,114.497,-42.6321,42.6321)
plt.plot(doubletIsoVX,doubletIsoVY,"b:")


#Define reco point
recoHitX = [-13.1384]
recoHitY = [14.7012]
plt.scatter(recoHitX,recoHitY,marker='o',c='green')


#Define truth point
truthX = [-13.0697]
truthY = [8.19153]
plt.scatter(truthX,truthY,marker='o',c='yellow')

#Display it
plt.show()

