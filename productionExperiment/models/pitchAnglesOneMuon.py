#Model vertical betatron oscillation for single mu+ and corresponding evolution of pitch angle
#Calculate resulting pitch correction for this one muon
#Note that this code is imported by by pitchAnglesMuonPopulation.py
#Tom Stuttard (12th Oct 2016) 

import numpy as np
import sys, datetime, math, random, argparse
#import pylab
import matplotlib.pyplot as plt
import mathtools


#
# Define generic/common params
#

#The ring
ringVerticalAcceptanceMm = 45.
fieldIndex = 0.175
cyclotronPeriodNs = 149.
verticalBetatronPeriodNs = cyclotronPeriodNs / math.sqrt(fieldIndex)

#Injection
t0Ns = 0.

#Physics constants
speedOfLightMperS = 299792458. #CODATA 2014
muonAnomoly = 11659203.e-10 #E821 value
muonRestMassGeV = 105.6583715e-3 #PDG 2014
muonRestLifetimeNs = 2.1969811e3 #PDG 2014

#
# Helper functions
#

#Calculate vertical position from vertical betatron oscillation for a given t [mm]
#TODO Add intial phase
def verticalBetatronPositionMm(verticalBetatronAmplitudeMm,verticalBetatronPeriodNs,t) :
  return verticalBetatronAmplitudeMm * math.cos( 2 * math.pi * t / verticalBetatronPeriodNs )

#Calculate vertical pitch from vertical betatron oscillation for a given t [rad]
#Pitch angle, psi = atan(dy/dz)
#dy/dz = - (2*pi*Ay/(c*T)) * sin(2*pi*t/T), where t=z/c (assuming particle travelling at c)
#TODO Add intial phase
def verticalBetatronPitchAngleRad(verticalBetatronAmplitudeMm,verticalBetatronPeriodNs,t) :
  dydz = -2. * math.pi * (verticalBetatronAmplitudeMm*1.e-3) * math.sin( 2 * math.pi * t / verticalBetatronPeriodNs ) / ( speedOfLightMperS * (verticalBetatronPeriodNs*1.e-9) )
  psiRad = math.atan(dydz)
  return psiRad

#Calculate pitch correction from list of pitch angle squared values in [rad^2]
def pitchCorrection(psi2ValsRad2) :
  averagePsi2Rad2 = sum(psi2ValsRad2) / float(len(psi2ValsRad2))
  pitchCorrection = -averagePsi2Rad2 / 2 #TDR equation 4.7
  pitchCorrectionPpm = ( pitchCorrection * 1.e6 ) / muonAnomoly
  return pitchCorrection,pitchCorrectionPpm

#
# One muon simulation
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  
  #
  # Define simulation params
  #

  #Betatron
  verticalBetatronAmplitudeMm = 10. #Max is 45 mm (e.g. max acceptance of storage ring)

  #Sim
  numPeriodsToDraw = 10
  numStepsPerPeriod = 1000
  numSteps = float(numPeriodsToDraw) * float(numStepsPerPeriod)
  stepSizeNs = float(numPeriodsToDraw) * verticalBetatronPeriodNs / float(numSteps)

  print ""
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
    y = verticalBetatronPositionMm(verticalBetatronAmplitudeMm,verticalBetatronPeriodNs,t)
    yValsMm.append(y)

    #Get pitch angle, psi = atan(dy/dz)
    psiRad = verticalBetatronPitchAngleRad(verticalBetatronAmplitudeMm,verticalBetatronPeriodNs,t)
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


  #
  # Calculate pitch correction
  #

  pitchCorrection, pitchCorrectionPpm = pitchCorrection(psi2ValsRad2)

  print ""
  print "Results:"
  print "  Pitch correction = %e (%f ppm for a_mu = %f)" % (pitchCorrection,pitchCorrectionPpm,muonAnomoly)
  print ""

