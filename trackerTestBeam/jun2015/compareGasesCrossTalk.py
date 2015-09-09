from ROOT import TFile, TCanvas, gStyle, TH1F
import os
import argparse
import RootHelper as rh
from collections import OrderedDict

#Define files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/'
inputFileName = 'mtestRecoAnalysis_eventSelectionPlots.root'
inputFiles = OrderedDict()
inputFiles['Ar-CO2 : Run 316'] = inputRootDir + 'run00316/deadTime150ns/' + inputFileName
inputFiles['Ar-Ethane : Run 405'] = inputRootDir + 'run00405/deadTime150ns/' + inputFileName

#Open all files (keep them in dict so have them in memory simultaneously)
rootFiles = OrderedDict()
for key, rootFileName in inputFiles.items() :
  rootFiles[key] = rh.openFile(rootFileName)


#
# Cross-talk in same layer
#


lbDir = 'EventSelection/Islands/LB0/'
asdq = 'TDC2ASDQ0'

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2)
#gStyle.SetOptStat(False)

#Loop over files
counter = 0
for key, rootFile in rootFiles.items() :

  #Get histogram hit time diffs in adjacent channels in same layer
  hist = rh.getFromFile(rootFile,lbDir+'h_digitTimeGapsInIslandAdjacentChannelsSameLayer'+asdq)
  counter += 1

  #Format histo
  hist.SetTitle(key+' : Same layer ;Hit time difference [ns];')
  hist.GetXaxis().SetRangeUser(-50.,100.)

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")


#
# Cross-talk in different layer
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2)

#Loop over files
counter = 0
for key, rootFile in rootFiles.items() :

  #Get histogram hit time diffs in adjacent channels in same layer
  hist = rh.getFromFile(rootFile,lbDir+'h_digitTimeGapsInIslandAdjacentChannelsDiffLayer'+asdq)
  counter += 1

  #Format histo
  hist.SetTitle(key+' : Different layer ;Hit time difference [ns];')
  hist.GetXaxis().SetRangeUser(-50.,100.)

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")

