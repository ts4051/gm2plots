#Plot data from SoftwareSpeedTest.py script outputfile
#Using AMC13 fake data mode to select data volume, so this only tests the AMC13->PC link and DAQ software, not the underlying boards
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
      print row

    #Return the data containers
    return payloadNumWords, eventNumWords, eventSizeMB, meanEventTimeMs, meanEventRateHz, meanDataRateMbps
      

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
  plt.title('')
  plt.xlabel('Event size [bytes]')
  plt.ylabel('Mean event processing [ms]')
  plt.plot(eventSizeMB,meanEventTimeMs,"b-")
  plt.show()

  #Plot data volume vs max event rate
  plt.title('')
  plt.xlabel('Event size [bytes]')
  plt.ylabel('Max event rate [Hz]')
  plt.plot(eventSizeMB,meanEventRateHz,"b-")
  plt.show()

  #Plot data volume vs max data rate
  plt.title('')
  plt.xlabel('Event size [bytes]')
  plt.ylabel('Max data rate [Mbps]')
  plt.plot(eventSizeMB,meanDataRateMbps,"b-")
  plt.show()

