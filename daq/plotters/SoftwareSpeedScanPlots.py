#Plot data from SoftwareSpeedScan.py script output file
#Tom Stuttard (23rd Nov 2016) 

import numpy as np
import sys, datetime, math, random, argparse
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.mlab as mlab
import mathtools
import csv

#Parse input file
def parseInputFile(inputFile) :

  #CSV file : Columns...
  #Fake payload size [64-bit words], Event size [64-bit words], Event size [MB], Mean event time [ms], Mean event rate [Hz], Mean data rate [Mbps]
  
  #Open file
  with open(inputFile, 'rb') as csvfile :

    #Parse CSV file into rows
    parsedFile = csv.reader(csvfile, delimiter=',', quotechar='#')

    #Loop over rows to fill a column for each list
    payloadNumWords = list()
    eventNumWords = list()
    eventSizeMB = list()
    meanEventTimeMs = list()
    meanEventRateHz = list()
    meanDataRateMbps = list()
    for row in parsedFile:
      payloadNumWords.append( int(row[0]) )
      eventNumWords.append( int(row[1]) )
      eventSizeMB.append( float(row[2]) )
      meanEventTimeMs.append( float(row[3]) )
      meanEventRateHz.append( float(row[4]) )
      meanDataRateMbps.append( float(row[5]) )

    #Return the data containers
    return np.array(payloadNumWords), np.array(eventNumWords), np.array(eventSizeMB), np.array(meanEventTimeMs), np.array(meanEventRateHz), np.array(meanDataRateMbps)
      

#
# Run simulation
# 

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #
  # Get data
  #

  #Get args
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('-i','--input-file', type=str, required=True, help='Input file', dest='inputFile')
  args = parser.parse_args()

  #Parse file
  payloadNumWords, eventNumWords, eventSizeMB, meanEventTimeMs, meanEventRateHz, meanDataRateMbps = parseInputFile(args.inputFile)


  #
  # Make plots
  #

  #Plot data volume vs max event rate
  plt.figure(facecolor='white')
  plt.title('')
  plt.xlabel('Event size [MB]')
  plt.ylabel('Mean event processing time [ms]')
  plt.plot(eventSizeMB,meanEventTimeMs,"b-")
  plt.legend()
  plt.grid()

  #Plot data volume vs max event rate
  plt.figure(facecolor='white')
  plt.title('')
  plt.xlabel('Event size [MB]')
  plt.ylabel('Max event rate [Hz]')
  plt.plot(eventSizeMB,meanEventRateHz,"b-")
  plt.axhline(12.,color="red",linestyle="--",label="Experiment fill rate")
  plt.axvline(1.2/8.,color="green",linestyle="--",label="Expected event size")
  plt.axvline(12.6/8.,color="magenta",linestyle="--",label="Max event size")
  plt.legend()
  plt.grid()

  #Plot data volume vs max data rate
  plt.figure(facecolor='white')
  plt.title('')
  plt.xlabel('Event size [MB]')
  plt.ylabel('Max data rate [Mbps]')
  plt.plot(eventSizeMB,meanDataRateMbps,"b-")
  plt.legend()
  plt.grid()

  plt.show()

