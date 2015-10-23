from ROOT import TFile, TCanvas, gStyle, TH1F
import os
import argparse
import RootHelper as rh
from collections import OrderedDict

#Define files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_coordSystems/data/testbeam/'
inputFileName = 'mtestRecoAnalysis_strawRecoPlots.root'
efficiencyScanFiles = OrderedDict()
inputFiles = OrderedDict()
inputFiles['Ar-CO2 : Run 316'] = inputRootDir + '/run00316/' + inputFileName
inputFiles['Ar-Ethane : Run 402'] = inputRootDir + '/run00402/' + inputFileName

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

  #Get hit map
  h_hitPos = rh.getFromFile(rootFile,'RecoHits/h_recoHitPosTransverse')
  counter += 1

  #Draw to canvas
  canvas.cd(counter)
  h_hitPos.SetTitle(key+' : Hit map ; Radial position [mm] ; Vertical position [ mm ]')
  h_hitPos.GetXaxis().SetRangeUser(-60.,40.)
  h_hitPos.GetYaxis().SetRangeUser(-50.,50.)
  #h_hitPos.SetStats(False)
  h_hitPos.Draw("CONT0")

raw_input("Press Enter to continue...")

