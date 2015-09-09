from ROOT import TFile, TCanvas, gStyle, TH1F, TGraph, TGraphErrors
import os
import argparse
import RootHelper as rh
from collections import OrderedDict

#Define files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/'
inputFileName = 'mtestRecoAnalysis_strawEfficiencyPlots.root'
efficiencyScanFiles = OrderedDict()
inputFiles = OrderedDict()
inputFiles[1500.] = inputRootDir + 'run00359/deadTime150ns/' + inputFileName
inputFiles[1600.] = inputRootDir + 'run00372/deadTime150ns/' + inputFileName
inputFiles[1700.] = inputRootDir + 'run00390/deadTime150ns/' + inputFileName
inputFiles[1800.] = inputRootDir + 'run00405/deadTime150ns/' + inputFileName

#Open all files (keep them in dict so have them in memory simultaneously)
rootFiles = OrderedDict()
for hv, rootFileName in inputFiles.iteritems() :
  print str(hv)+'V',':',rootFileName
  rootFiles[hv] = rh.openFile(rootFileName)


#
# Num digits in island histo
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2,2)
#gStyle.SetOptStat(False)

#Loop over files
counter = 0
for hv, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawEfficiency/h_numDigitsInIsland')
  counter += 1

  #Format histo
  hist.SetTitle(str(hv)+'V ; Num digits in island;')

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")

#TODO num islands

#TODO num hits

#
# Mean digits in island
#

#Create a fresh canvas
canvas = TCanvas()

#Create graph
g_meanNumDigitsInIsland = TGraphErrors(len(inputFiles))
g_meanNumDigitsInIsland.SetTitle('Mean num digits in island; HV [V] ; <# digits in island>')
g_meanNumDigitsInIsland.SetMarkerStyle(2)
g_meanNumDigitsInIsland.SetMarkerSize(3)

#Loop over files
counter = 0
for hv, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawEfficiency/h_numDigitsInIsland')

  #Get mean # digits
  meanNumDigitsInIsland = hist.GetMean()
  errorNumDigitsInIsland = hist.GetRMS()

  #Add point to graph
  g_meanNumDigitsInIsland.SetPoint(counter,hv,meanNumDigitsInIsland)
  #g_meanNumDigitsInIsland.SetPointError(counter,0,errorNumDigitsInIsland)

  counter += 1

#Draw graph
g_meanNumDigitsInIsland.Draw()

raw_input("Press Enter to continue...")


#
# Mean # digits in MTest spill
#

#Create a fresh canvas
canvas = TCanvas()

#Create graph
g_meanNumDigitsInSpill = TGraphErrors(len(inputFiles))
g_meanNumDigitsInSpill.SetTitle('Mean num digits in spill; HV [V] ; <# digits in spill>')
#g_meanNumDigitsInSpill.SetMarkerStyle(2)
#g_meanNumDigitsInSpill.SetMarkerSize(3)

#Loop over files
counter = 0
for hv, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawEfficiency/h_totalDigits')

  #Get mean # digits
  meanNumDigitsInSpill = hist.GetMean()
  errorNumDigitsInSpill= hist.GetRMS()

  #Add point to graph
  g_meanNumDigitsInSpill.SetPoint(counter,hv,meanNumDigitsInSpill)
  g_meanNumDigitsInSpill.SetPointError(counter,0,errorNumDigitsInSpill)

  counter += 1

#Draw graph
g_meanNumDigitsInSpill.Draw()

raw_input("Press Enter to continue...")


#
# Mean # islands in MTest spill
#

#Create a fresh canvas
canvas = TCanvas()

#Create graph
g_meanNumIslandsInSpill = TGraphErrors(len(inputFiles))
g_meanNumIslandsInSpill.SetTitle('Mean num islands in spill; HV [V] ; <# islands in spill>')
#g_meanNumIslandsInSpill.SetMarkerStyle(2)
#g_meanNumIslandsInSpill.SetMarkerSize(3)

#Loop over files
counter = 0
for hv, rootFile in rootFiles.items() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'StrawEfficiency/h_totalIslands')

  #Get mean # digits
  meanNumIslandsInSpill = hist.GetMean()
  errorNumIslandsInSpill= hist.GetRMS()

  #Add point to graph
  g_meanNumIslandsInSpill.SetPoint(counter,hv,meanNumIslandsInSpill)
  g_meanNumIslandsInSpill.SetPointError(counter,0,errorNumIslandsInSpill)

  counter += 1

#Draw graph
g_meanNumIslandsInSpill.Draw()

raw_input("Press Enter to continue...")

