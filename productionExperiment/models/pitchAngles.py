#Model mu+ pitch angle

import numpy as np
import sys, datetime, math, random, argparse
#import pylab
import matplotlib.pyplot as plt
import mathtools


#
# Define params
#

#The ring
fieldIndex = 0.175
cyclotronPeriodNs = 149.
verticalBetatronAmplitudeMm = 45. #Max is 45 mm (e.g. max acceptance of stroage ring)

#Sim
numPeriodsToDraw = 5
numStepsPerPeriod = 100
t0Ns = 0.

#Physics constants
speedOfLightMperS = 3.e8
amu = 0.00116592

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
psi2ValsRad2 = list()

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
  psi2ValsRad2.append(psiRad*psiRad)


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


#
# Plot pitch angle squared vs t
#

plt.title('')
plt.xlabel('Time [ns]')
plt.ylabel('Pitch angle squared [rad^2]')
plt.plot(tValsNs,psi2ValsRad2,"b-")
plt.show()


#
# Calculate pitch correction
#

averagePsi2Rad2 = sum(psi2ValsRad2) / float(len(psi2ValsRad2))
pitchCorrection = -averagePsi2Rad2 / 2 #TDR equation 4.7
pitchCorrectionPpm = ( pitchCorrection * 1.e6 ) / amu

print ""
print "Pitch correction = %e (%f ppm for a_mu = %f)" % (pitchCorrection,pitchCorrectionPpm,amu)
print ""

