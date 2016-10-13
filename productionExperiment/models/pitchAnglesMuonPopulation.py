#Model pitch angle due to vertical betatron oscillation for a population of mu+
#Calculate resulting overall pitch correction
#Tom Stuttard (12th Oct 2016) 

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
injectionYMeanMm = 0. 
injectionYSigmaMm = 10. #TODO
ringVerticalAcceptanceMm = 45.

#Sim
numMuons = 100000
t0Ns = 0.
debug = False

#Physics constants
speedOfLightMperS = 299792458. #CODATA 2014
muonAnomoly = 11659203.e-10 #E821 value
muonRestMassGeV = 105.6583715e-3 #PDG 2014
muonRestLifetimeNs = 2.1969811e3

#Derived
verticalBetatronPeriodNs = cyclotronPeriodNs / math.sqrt(fieldIndex)

print ""
print "Params:"
print "  Num mu+ = %i" % (numMuons)
print "  n = %f" % (fieldIndex)
print ""

#
# Generate data
#

#Init containers
injectionYValsMm = list()
injectionMomentumValsGeV = list()
injectionTimeValsNs = list()
timeInRingValsNs = list()
decayTimeValsNs = list()
decayYValsMm = list()
decayPitchAngleValsDeg = list()
decayPitchAngle2ValsRad2 = list()

#Loop over mu+
for i_mu in range(0,numMuons) :

  #Generate injection y (truncate around max acceptance)
  while True :
    injectionYMm = random.gauss(injectionYMeanMm,injectionYSigmaMm)
    if abs(injectionYMm) < ringVerticalAcceptanceMm : break
  injectionYValsMm.append(injectionYMm)

  #Generate momentum
  pGeV = 3.09 #TODO Spread
  injectionMomentumValsGeV.append(pGeV)

  #Get boost from momentum
  gamma = pGeV / muonRestMassGeV

  #Generate injection time
  injectionTimeNs = 0.
  #TODO spread, W function
  injectionTimeValsNs.append(injectionTimeNs)

  #Generate decay time (get dilated lifetime and generate decay from exponetial using this as time constant)
  lifetimeNs = gamma * muonRestLifetimeNs
  timeInRingNs = -1. * lifetimeNs * math.log( random.uniform(0.,1.) )
  timeInRingValsNs.append(timeInRingNs)
  decayTimeNs = injectionTimeNs + timeInRingNs
  decayTimeValsNs.append(decayTimeNs)

  #Get y at decay time (vertical BO amplitude is displacement from orbit plane at injection)
  #Only oscillate during time in ring (e.g. don't include injection time)
  verticalBetatronAmplitudeMm = injectionYMm
  decayYMm = verticalBetatronAmplitudeMm * math.cos( 2 * math.pi * timeInRingNs / verticalBetatronPeriodNs ) #TODO Correct betatron period for cyclotron variation with boost
  decayYValsMm.append(decayYMm)

  #Get pitch angle at time of decay, psi = atan(dy/dz)
  # dy/dz = - (2*pi*Ay/(c*T)) * sin(2*pi*t/T), where t=z/c (assuming particle travelling at c) #TODO calculate v from boost
  dydz = -2. * math.pi * (verticalBetatronAmplitudeMm*1.e-3) * math.sin( 2 * math.pi * timeInRingNs / verticalBetatronPeriodNs ) / ( speedOfLightMperS * (verticalBetatronPeriodNs*1.e-9) )
  psiRad = math.atan(dydz)
  decayPitchAngleValsDeg.append( math.degrees(psiRad) )
  decayPitchAngle2ValsRad2.append(psiRad*psiRad)

  
  #TODO generate full path, bot just decay point to check pitch

  if debug : 
    print "mu+ %i : Injection y = %f [mm] : Decay y = %f [mm] : Pitch angle = %f [deg]" \
      % (i_mu,injectionYMm,decayYMm,math.degrees(psiRad))



#
# Plot injection profile
#

plt.xlabel('Injection y [mm]')
plt.hist(injectionYValsMm, normed=False, bins=20)
plt.show()

plt.xlabel('Injection momentum [GeV]')
plt.hist(injectionMomentumValsGeV, normed=False, bins=20)
plt.show()

plt.xlabel('Injection time [ns]')
plt.hist(injectionTimeValsNs, normed=False, bins=20)
plt.show()


#
# Plot decay profile
#

plt.xlabel('Decay y [mm]')
plt.hist(decayYValsMm, normed=False, bins=20)
plt.show()

plt.xlabel('Decay time in ring [ns]')
plt.hist(timeInRingValsNs, normed=False, bins=20)
plt.show()

plt.xlabel('Decay absolute time [ns]')
plt.hist(decayTimeValsNs, normed=False, bins=20)
plt.show()

plt.xlabel('Decay pitch angle [deg]')
plt.hist(decayPitchAngleValsDeg, normed=False, bins=20)
plt.show()

plt.xlabel('Decay pitch angle squared [rad^2]')
plt.hist(decayPitchAngle2ValsRad2, normed=False, bins=20)
plt.show()

'''
#
# Plot decay y vs t
#

plt.title('')
plt.xlabel('Decay time [ns]')
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
# Histogram pitch angle
#

plt.xlabel('Pitch angle [deg]')
plt.hist(psiValsDeg, normed=False, bins=20)
plt.show()

#
# Plot pitch angle squared vs t
#

plt.title('')
plt.xlabel('Time [ns]')
plt.ylabel('Pitch angle squared [rad^2]')
plt.plot(tValsNs,psi2ValsRad2,"b-")
plt.show()

'''
#
# Calculate pitch correction
#

averageDecayPitchAngle2ValsRad2 = sum(decayPitchAngle2ValsRad2) / float(len(decayPitchAngle2ValsRad2)) #TODO use total average, not just from decay
pitchCorrection = -averageDecayPitchAngle2ValsRad2 / 2 #TDR equation 4.7
pitchCorrectionPpm = ( pitchCorrection * 1.e6 ) / muonAnomoly

print ""
print "Results:"
print "  Pitch correction = %e (%f ppm for a_mu = %f)" % (pitchCorrection,pitchCorrectionPpm,muonAnomoly)
print ""

