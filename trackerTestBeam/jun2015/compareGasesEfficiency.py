from ROOT import TFile, TCanvas, gStyle, TH1F
import os
import argparse
import RootHelper as rh
from collections import OrderedDict

#Define files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/'
inputFileName = 'mtestRecoAnalysis_strawEfficiencyPlots.root'
efficiencyScanFiles = OrderedDict()
inputFiles = OrderedDict()
inputFiles['Ar-CO2 : Run 316'] = inputRootDir + 'run00316/deadTime150ns/' + inputFileName
inputFiles['Ar-Ethane : Run 405'] = inputRootDir + 'run00405/deadTime150ns/' + inputFileName

#Open all files (keep them in dict so have them in memory simultaneously)
rootFiles = OrderedDict()
for key, rootFileName in inputFiles.iteritems() :
  print key,':',rootFileName
  rootFiles[key] = rh.openFile(rootFileName)


#
# Num digits in island histo
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2)
#gStyle.SetOptStat(False)

#Loop over files
counter = 0
for key, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawEfficiency/h_numDigitsInIsland')
  counter += 1

  #Format histo
  hist.SetTitle(key+';Num digits in island;')

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")


#
# Num seeds in island histo
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2)

#Loop over files
counter = 0
for key, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawEfficiency/h_numSeedsFormedFromIsland')
  counter += 1

  #Format histo
  hist.SetTitle(key+';Num seeds formed from island;')

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")


#
# Read/reco steps # digit summaries
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2)

#Loop over files
counter = 0
for key, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawEfficiency/h_summary')
  counter += 1

  #Format histo
  hist.SetTitle(key)
  hist.GetYaxis().SetRangeUser(0.,200.e3)
  hist.SetStats(False)

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")
