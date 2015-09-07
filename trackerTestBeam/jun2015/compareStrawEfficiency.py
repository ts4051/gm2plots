from ROOT import TFile, TCanvas, gStyle, TH1F
import os
import argparse
import RootHelper as rh

#Define files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/sim/'
inputFileName = 'mtestRecoAnalysis_strawEfficiencyPlots.root'
efficiencyScanFiles = dict()
efficiencyScanFiles[0.25] = inputRootDir + 'strawEff25/' + inputFileName
efficiencyScanFiles[0.5] = inputRootDir + 'strawEff50/' + inputFileName
efficiencyScanFiles[0.75] = inputRootDir + 'strawEff75/' + inputFileName
efficiencyScanFiles[1.] = inputRootDir + 'strawEff100/' + inputFileName

#Open all files (keep them in dict so have them in memory simultaneously)
rootFiles = dict()
for efficiency, rootFileName in efficiencyScanFiles.iteritems() :
  rootFiles[efficiency] = rh.openFile(rootFileName)


#
# Num digits in island histo
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2,2)
#gStyle.SetOptStat(False)

#Loop over files
counter = 0
for efficiency, rootFile in rootFiles.iteritems() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawEfficiency/h_numDigitsInIsland')
  counter += 1

  #Format histo
  hist.SetTitle('Efficiency = '+str(efficiency)+';Num digits in island;')

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")


#
# Num seeds in island histo
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2,2)

#Loop over files
counter = 0
for efficiency, rootFile in rootFiles.iteritems() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawEfficiency/h_numSeedsFormedFromIsland')
  counter += 1

  #Format histo
  hist.SetTitle('Efficiency = '+str(efficiency)+';Num seeds formed from island;')

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")
