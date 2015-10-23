from ROOT import TFile, TCanvas, gStyle, TH1F
import os
import argparse
import RootHelper as rh
from collections import OrderedDict

#Define files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/'
inputFileName = 'mtestDigitsAnalysis_strawTriggerDigitPlots.root'
efficiencyScanFiles = OrderedDict()
inputFiles = OrderedDict()
inputFiles['Ar-CO2 : Run 314'] = inputRootDir + 'run00316/deadTime150ns/' + inputFileName
inputFiles['Ar-Ethane : Run 404'] = inputRootDir + 'run00404/deadTime150ns/' + inputFileName
#inputFiles['Ar-Ethane : Run 405'] = inputRootDir + 'run00405/deadTime150ns/' + inputFileName


#Open all files (keep them in dict so have them in memory simultaneously)
rootFiles = OrderedDict()
for key, rootFileName in inputFiles.iteritems() :
  print key,':',rootFileName
  rootFiles[key] = rh.openFile(rootFileName)


#
# Global layer number for hit histo
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2)

#Loop over files
counter = 0
for key, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawDigits/h_globalLayer')
  counter += 1

  #Normalise to max bin
  maxBinContent = hist.GetBinContent( hist.GetMaximumBin() )
  for i_bin in range(1,hist.GetNbinsX()+1) : #Bin range starts at 1, not 0
    newBinContent = hist.GetBinContent(i_bin) / maxBinContent
    hist.SetBinContent( i_bin, newBinContent )

  #Format histo
  hist.SetTitle(key)
  hist.GetXaxis().SetTitle('Layer number of hit')
  hist.GetYaxis().SetTitle('[Fraction of max]')
  hist.GetYaxis().SetRangeUser(0.,1.1)
  hist.GetYaxis().SetTitleOffset(1.4)
  hist.SetStats(False)

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")
