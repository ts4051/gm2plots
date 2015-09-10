from ROOT import TFile, TCanvas, gStyle, TH1F
import os
import argparse
import RootHelper as rh
from collections import OrderedDict

#Define files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/'
inputFileName = 'mtestDigitsAnalysis_strawTriggerDigitPlots.root'
inputFiles = OrderedDict()
inputFiles['Ar-CO2 : Run 316'] = inputRootDir + 'run00316/deadTime150ns/' + inputFileName
inputFiles['Ar-Ethane : Run 405'] = inputRootDir + 'run00405/deadTime150ns/' + inputFileName

#Open all files (keep them in dict so have them in memory simultaneously)
rootFiles = OrderedDict()
for key, rootFileName in inputFiles.items() :
  print key,':',rootFileName
  rootFiles[key] = rh.openFile(rootFileName)


#
# Drift time diff histo
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2)
#gStyle.SetOptStat(False)

#Loop over files
counter = 0
for key, rootFile in rootFiles.items() :

  #Get histogram for hottest straw pair (U1_S11 is hottest straw, paried with either U0_S11 or 12 for doublet)
  hottestStrawDir = 'StrawDigits/Station_0/Module_0/View_0/Layer_1/Wire_11/' #Hottest straw
  hist = rh.getFromFile(rootFile,hottestStrawDir+'h_hitTimeDiff_S0_M0_V0_L0_W11') #Completes hottest doublet
  counter += 1

  #Format histo
  hist.SetTitle(key+';Hit time difference [ns];')
  #hist.GetXaxis().SetRangeUser(-100.,100.)

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")

