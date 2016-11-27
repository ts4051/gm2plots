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
  #Fake payload size [64-bit words], Event size [64-bit words], Event size [MB], Event time taken [ms]
  
  #Open file
  with open(inputFile, 'rb') as csvfile :

    #Parse CSV file into rows
    parsedFile = csv.reader(csvfile, delimiter=',', quotechar='#')

    #Loop over rows to fill a column for each list
    payloadNumWords = list()
    eventNumWords = list()
    eventSizeMB = list()
    eventTimeTakenMs = list()
    meanEventRateHz = list()
    meanDataRateMbps = list()
    for row in parsedFile:
      payloadNumWords.append( int(row[0]) )
      eventNumWords.append( int(row[1]) )
      eventSizeMB.append( float(row[2]) )
      eventTimeTakenMs.append( float(row[3]) )

    #Return the data containers
    return payloadNumWords, eventNumWords, eventSizeMB, eventTimeTakenMs
      

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
  payloadNumWords, eventNumWords, eventSizeMB, eventTimeTakenMs = parseInputFile(args.inputFile)


  #
  # Make plots
  #

  #Plot all event time points
  plt.figure(facecolor='white')
  plt.title('')
  plt.xlabel('Event num')
  plt.ylabel('Event time taken [ms]')
  plt.plot(eventTimeTakenMs,"b-")
  plt.show()

  plt.figure(facecolor='white')
  plt.title('')
  plt.xlabel('Event time taken [ms]')
  plt.hist(eventTimeTakenMs, normed=False, bins=50)
  plt.show()


