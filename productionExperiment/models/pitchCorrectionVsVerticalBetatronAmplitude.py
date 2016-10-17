#Determine how pitch corrections change versus vetical betatron amplitude
#Note that the vertical betatron amplitude depends on injection y and injection pitch angle
#Tom Stuttard (13th Oct 2016) 

import numpy as np
import sys, datetime, math, random, argparse
#import pylab
import matplotlib.pyplot as plt
import mathtools

#Import common functions from other pitch angle toy MC
import pitchAnglesOneMuon


#
# Simulation
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #
  # Define params
  #

  #Sim
  numPeriodsToDraw = 5
  numStepsPerPeriod = 1000
  numSteps = float(numPeriodsToDraw) * float(numStepsPerPeriod)
  stepSizeNs = float(numPeriodsToDraw) * pitchAnglesOneMuon.verticalBetatronPeriodNs / float(numSteps)
  t0Ns = 0.

  #
  # Top-level data containers
  #

  pitchCorrectionValsPpb = list()


  #
  # Loop over vertical betatron amplitudes
  #

  verticalBetatronAmplitudeValsMm = range(0.,45.)

  for verticalBetatronAmplitudeMm in verticalBetatronAmplitudeValsMm :

    #
    # Generate data for this vertical betatron amplitude
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
      y = pitchAnglesOneMuon.verticalBetatronPositionMm(verticalBetatronAmplitudeMm,pitchAnglesOneMuon.verticalBetatronPeriodNs,t)
      yValsMm.append(y)

      #Get pitch angle, psi = atan(dy/dz)
      psiRad = pitchAnglesOneMuon.verticalBetatronPitchAngleRad(verticalBetatronAmplitudeMm,pitchAnglesOneMuon.verticalBetatronPeriodNs,t)
      psiValsDeg.append( math.degrees(psiRad) )
      psi2ValsRad2.append(psiRad*psiRad)


    #
    # Calculate pitch correction for this injection y value
    #

    pitchCorrection, pitchCorrectionPpb = pitchAnglesOneMuon.pitchCorrection(psi2ValsRad2)
    pitchCorrectionValsPpb.append(pitchCorrectionPpb)


  #
  # Plot decay y vs t
  #

  plt.title('')
  plt.xlabel('Vertical betatron amplitude [mm]')
  plt.ylabel('Pitch correction [ppb]')
  plt.plot(verticalBetatronAmplitudeValsMm,pitchCorrectionValsPpb,"r-")
  plt.show()

