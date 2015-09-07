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

#Create canvas
canvas = TCanvas()
canvas.Divide(2,2)
#gStyle.SetOptStat(False)

#Loop over files (keep them in list so have them in memory simultaneously)
rootFiles = list()
counter = 0
for efficiency, rootFileName in efficiencyScanFiles.iteritems() :

  #Open file and get histogram
  rootFiles.append( rh.openFile(rootFileName) )
  hist = rh.getFromFile(rootFiles[-1],'StrawEfficiency/Islands/h_numDigitsInIsland')

  counter += 1

  #Format histo
  hist.SetTitle('Efficiency = '+str(efficiency)+';Num digits in island;')

  ##Draw to cnavas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")


