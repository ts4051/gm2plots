#Model pitch angle due to vertical betatron oscillation for a population of mu+
#Calculate resulting overall pitch correction
#Tom Stuttard (12th Oct 2016) 

import numpy as np
import sys, datetime, math, random, argparse
#import pylab
import matplotlib.pyplot as plt
import mathtools

#Import common functions from other pitch angle toy MC
import pitchAnglesOneMuon


#
# Simulation function
#

#Function to generate a muon distribution and model the params
def muonPopulationPitchAnglesModel(numMuons,injectionYMeanMm,injectionYSigmaMm,injectionTimeWidthNs,plot=True,debug=False) :

  print ""
  print "Params:"
  print "  Num mu+ = %i" % (numMuons)
  print "  n = %f" % (pitchAnglesOneMuon.fieldIndex)
  print "  Ring vertical acceptance = %f [mm]" % (pitchAnglesOneMuon.ringVerticalAcceptanceMm)
  print "  Gaussian vertical injection profile : Mean = %f [mm] : Sigma = %f [mm]" % (injectionYMeanMm,injectionYSigmaMm)
  print ""

  #
  # Data containers
  #

  injectionYValsMm = list()
  injectionMomentumValsGeV = list()
  injectionTimeValsNs = list()
  timeInRingValsNs = list()
  decayTimeValsNs = list()
  decayYValsMm = list()
  decayPitchAngleValsDeg = list()
  decayPitchAngle2ValsRad2 = list()


  #
  # Generate data
  #

  #Loop over mu+
  for i_mu in range(0,numMuons) :

    #Generate injection y (truncate around max acceptance)
    while True :
      injectionYMm = random.gauss(injectionYMeanMm,injectionYSigmaMm)
      if abs(injectionYMm) < pitchAnglesOneMuon.ringVerticalAcceptanceMm : break
    injectionYValsMm.append(injectionYMm)

    #Generate momentum
    pGeV = 3.09 #TODO Spread
    injectionMomentumValsGeV.append(pGeV)

    #Get boost from momentum
    gamma = pGeV / pitchAnglesOneMuon.muonRestMassGeV

    #Generate injection time
    injectionTimeNs = random.uniform(0.,injectionTimeWidthNs)
    #TODO spread, W function
    injectionTimeValsNs.append(injectionTimeNs)

    #Generate decay time (get dilated lifetime and generate decay from exponetial using this as time constant)
    lifetimeNs = gamma * pitchAnglesOneMuon.muonRestLifetimeNs
    timeInRingNs = -1. * lifetimeNs * math.log( random.uniform(0.,1.) )
    timeInRingValsNs.append(timeInRingNs)
    decayTimeNs = injectionTimeNs + timeInRingNs
    decayTimeValsNs.append(decayTimeNs)

    #Get y at decay time (vertical BO amplitude is displacement from orbit plane at injection) 
    #Only oscillate during time in ring (e.g. don't include injection time)
    verticalBetatronAmplitudeMm = injectionYMm
    decayYMm = pitchAnglesOneMuon.verticalBetatronPositionMm(verticalBetatronAmplitudeMm,pitchAnglesOneMuon.verticalBetatronPeriodNs,timeInRingNs)
    decayYValsMm.append(decayYMm)

    #Get pitch angle at time of decay, psi
    psiRad = pitchAnglesOneMuon.verticalBetatronPitchAngleRad(verticalBetatronAmplitudeMm,pitchAnglesOneMuon.verticalBetatronPeriodNs,timeInRingNs)
    decayPitchAngleValsDeg.append( math.degrees(psiRad) )
    decayPitchAngle2ValsRad2.append(psiRad*psiRad)
  
    #TODO generate full path, not just decay point to check pitch

    #Dump debug info
    if debug : 
      print "mu+ %i : Injection y = %f [mm] : Decay y = %f [mm] : Pitch angle = %f [deg]" \
        % (i_mu,injectionYMm,decayYMm,math.degrees(psiRad))


  #
  # Plot injection profile
  #

  if plot :

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

  if plot :

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


  #
  # Plot decay y vs t
  #

  if plot :

    plt.title('')
    plt.xlabel('Decay time [ns]')
    plt.ylabel('Decay y [mm]')
    plt.plot(decayTimeValsNs,decayYValsMm,"b.")
    plt.xlim([0,1000])
    plt.show()

    plt.title('')
    plt.xlabel('Time in ring [ns]')
    plt.ylabel('Decay y [mm]')
    plt.plot(timeInRingValsNs,decayYValsMm,"b.")
    plt.xlim([0,1000])
    plt.show()


  #
  # Plot decay pitch angle vs t
  #

  if plot :

    plt.title('')
    plt.xlabel('Decay time [ns]')
    plt.ylabel('Decay pitch angle [deg]')
    plt.plot(decayTimeValsNs,decayPitchAngleValsDeg,"b.")
    plt.xlim([0,1000])
    plt.show()

    plt.title('')
    plt.xlabel('Time in ring [ns]')
    plt.ylabel('Decay pitch angle [deg]')
    plt.plot(timeInRingValsNs,decayPitchAngleValsDeg,"b.")
    plt.xlim([0,1000])
    plt.show()


  #
  # Calculate pitch correction
  #

  pitchCorrection, pitchCorrectionPpb = pitchAnglesOneMuon.pitchCorrection(decayPitchAngle2ValsRad2)

  print ""
  print "Results:"
  print "  Pitch correction = %f [ppb]" % (pitchCorrectionPpb)
  print ""


  #
  # Done
  #

  #Return results
  return pitchCorrectionPpb


#
# Run simulation
# 

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #
  # Define params
  #

  #Injection
  injectionYMeanMm = 0. 
  injectionYSigmaMm = 8.
  injectionTimeWidthNs = 120. #TODO W function

  #Sim
  numMuons = 100000
  debug = False

  #
  # Do simulation
  #

  #Call function that performs simulation for given input params
  muonPopulationPitchAnglesModel(numMuons,injectionYMeanMm,injectionYSigmaMm,injectionTimeWidthNs,debug=debug)

