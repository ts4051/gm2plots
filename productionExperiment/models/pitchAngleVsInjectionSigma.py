#Determine how pitch corrections change versus injection y distribution sigma (Gaussian)
#Tom Stuttard (13th Oct 2016) 

import numpy as np
import sys, datetime, math, random, argparse
#import pylab
import matplotlib.pyplot as plt
import mathtools

#Import common functions from other pitch angle toy MCs
import pitchAnglesOneMuon, pitchAnglesMuonPopulation


#
# Simulation
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #
  # Define params
  #

  #Injection
  injectionYMeanMm = 0. 
  injectionTimeWidthNs = 120. #TODO W function

  #Sim
  numMuons = 100000

  #
  # Top-level data containers
  #

  pitchCorrectionValsPpb = list()


  #
  # Loop over injection y RMS
  #

  #Injection params
  injectionYSigmaValsMm = range(0.,30.)

  for injectionYSigmaMm in injectionYSigmaValsMm :

    #Call function that performs simulation for given input params
    pitchCorrectionPpb = pitchAnglesMuonPopulation.muonPopulationPitchAnglesModel( \
      numMuons,injectionYMeanMm,injectionYSigmaMm,injectionTimeWidthNs,plot=False,debug=False)
    pitchCorrectionValsPpb.append(pitchCorrectionPpb)


  #
  # Plot decay y vs t
  #

  plt.title('')
  plt.xlabel('Injection distribution y sigma [mm]')
  plt.ylabel('Pitch correction [ppb]')
  plt.plot(injectionYSigmaValsMm,pitchCorrectionValsPpb,"r-")
  plt.show()

