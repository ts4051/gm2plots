from ROOT import TFile, TCanvas, gStyle, TH1F
import os
import argparse
import RootHelper as rh
from collections import OrderedDict

#Define files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/sim/MO_80_15_5-Eff_80/'
inputFiles = OrderedDict()
inputFiles['Before cut'] = inputRootDir + 'mtestRecoAnalysis_strawRecoPlots.root'
inputFiles['After cut'] = inputRootDir + 'mtestRecoAnalysis_strawRecoPlots.root'

#Open all files (keep them in dict so have them in memory simultaneously)
rootFiles = OrderedDict()
for key, rootFileName in inputFiles.iteritems() :
  print key,':',rootFileName
  rootFiles[key] = rh.openFile(rootFileName)


#
# Num reco hits
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2,2)
#gStyle.SetOptStat(False)

#Loop over files
counter = 0
for key, rootFile in rootFiles.iteritems() :

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
