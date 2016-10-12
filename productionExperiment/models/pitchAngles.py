#Model mu+ pitch angle

import numpy as np
import sys, datetime, math, random, argparse
#import pylab
import matplotlib.pyplot as plt
import mathtools


#
# Define params
#

#User defined
fieldIndex = 0.175
cyclotronPeriodNs = 149.
verticalBetatronAmplitudeMm = 45. #Max is 45 mm (e.g. max acceptance of stroage ring)
numPeriodsToDraw = 5
numStepsPerPeriod = 100
t0Ns = 0.
speedOfLightMperS = 3.e8

#Derived
verticalBetatronPeriodNs = cyclotronPeriodNs / math.sqrt(fieldIndex)
numSteps = float(numPeriodsToDraw) * float(numStepsPerPeriod)
stepSizeNs = float(numPeriodsToDraw) * verticalBetatronPeriodNs / float(numSteps)

print "Params:"
print "  n = %f" % (fieldIndex)
print "  Ty = %f ns" % (verticalBetatronPeriodNs)
print "  Ay = %f mm" % (verticalBetatronAmplitudeMm)
print ""

#
# Generate data
#

#Init containers
tValsNs = list()
yValsMm = list()
psiValsDeg = list()

#Loop over steps
for i in range(0,numSteps) :

  #Get t
  t = t0Ns + ( float(i) * stepSizeNs )
  tValsNs.append(t)

  #Get y
  y = verticalBetatronAmplitudeMm * math.cos( 2 * math.pi * t / verticalBetatronPeriodNs )
  yValsMm.append(y)

  #Get pitch angle, psi = atan(dy/dz)
  # dy/dz = - (2*pi*Ay/(c*T)) * sin(2*pi*t/T), where t=z/c (assuming particle travelling at c)
  dydz = -2. * math.pi * (verticalBetatronAmplitudeMm*1.e-3) * math.sin( 2 * math.pi * t / verticalBetatronPeriodNs ) / ( speedOfLightMperS * (verticalBetatronPeriodNs*1.e-9) )
  psiRad = math.atan(dydz)
  psiValsDeg.append( math.degrees(psiRad) )


#
# Plot y vs t
#

plt.title('')
plt.xlabel('Time [ns]')
plt.ylabel('y [mm]')
#plt.scatter(tVals,yVals,c='blue')
plt.plot(tValsNs,yValsMm,"b-")
plt.show()


#
# Plot pitch angle vs t
#

plt.title('')
plt.xlabel('Time [ns]')
plt.ylabel('Pitch angle [deg]')
plt.plot(tValsNs,psiValsDeg,"b-")
plt.show()


