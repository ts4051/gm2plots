from ROOT import TFile, TCanvas, gStyle, TH1F
import os
import argparse
import RootHelper as rh
from collections import OrderedDict

#Define files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/'
inputFileName = 'mtestRecoAnalysis_eventSelectionPlots.root'
efficiencyScanFiles = OrderedDict()
inputFiles = OrderedDict()
inputFiles['Sim : 0% cross-talk'] = inputRootDir + '/sim/strawEff40/MO-60-30-8-2/deadTime150ns/' + inputFileName
inputFiles['Sim : 1% cross-talk'] = inputRootDir + '/sim/strawEff40/MO-60-30-8-2/deadTime150ns_crossTalk1/' + inputFileName
inputFiles['Sim : 5% cross-talk'] = inputRootDir + '/sim/strawEff40/MO-60-30-8-2/deadTime150ns_crossTalk5/' + inputFileName

#Open all files (keep them in dict so have them in memory simultaneously)
rootFiles = OrderedDict()
for key, rootFileName in inputFiles.iteritems() :
  print key,':',rootFileName
  rootFiles[key] = rh.openFile(rootFileName)


#
# Cross-talk in same layer
#

strawDir = 'EventSelection/Islands/Station_0/'

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(3)

#Loop over files
counter = 0
for key, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,strawDir+'h_digitTimeGapsInIslandNearestNeighbourStrawSameLayer')
  counter += 1

  #Format histo
  hist.SetTitle(key+' : Same layer ; Hit time difference [ns];')
  hist.GetXaxis().SetRangeUser(-50.,100.)
  hist.GetYaxis().SetRangeUser(-0.,200.)

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")


#
# Cross-talk in other layer
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(3)

#Loop over files
counter = 0
for key, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,strawDir+'h_digitTimeGapsInIslandNearestNeighbourStrawDifferentLayer')
  counter += 1

  #Format histo
  hist.SetTitle(key+' : Different layer ; Hit time difference [ns];')
  hist.GetXaxis().SetRangeUser(-50.,100.)
  hist.GetYaxis().SetRangeUser(-0.,200.)

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")

