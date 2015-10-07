from ROOT import TFile, TCanvas, gStyle, TH1F
import os
#import argparse
import RootHelper as rh

#Define files to read
inputRootDir = '/home/tstuttard/physics/g-2/software/offline/gm2Dev_v6_01_00_testbeam/data/simplestCase_testSiStrawT0/'
recoHitsFileName = mtestRecoAnalysis_strawRecoPlots.root
goodRecoHitsFileName = mtestRecoAnalysis_strawGoodRecoPlots.root
inputFileNames = dict() #TODO Ordered
inputFileNames['Reco hits'] = inputRootDir + recoHitsFileName
inputFileNames['Good reco hits'] = inputRootDir + goodRecoHitsFileName

#Open all files (keep them in dict so have them in memory simultaneously)
rootFiles = dict() #TODO Ordered
for key, rootFileName in inputFileNames.iteritems() :
  rootFiles[key] = rh.openFile(rootFileName)


#
# Track time difference between doublets
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2)

#Loop over files
counter = 0
for key, rootFile in rootFiles.iteritems() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'Doublets/h_doubletTrackTimeDiff')
  counter += 1

  #Format histo
  hist.SetTitle(key+' : t0 (track time) difference between two doublets in reco hit ; t0 diff [ns]')

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")


#
# Num reco his in island
#

#Create a fresh canvas
canvas = TCanvas()
canvas.Divide(2)

#Loop over files
counter = 0
for key, rootFile in rootFiles.iteritems() :

  #Get histogram
  hist = rh.getFromFile(rootFile,'RecoHits/h_numRecoHitsInIsland')
  counter += 1

  #Format histo
  hist.SetTitle(key+' : Num reco hits in time island ; # reco hits [ns]')

  #Draw to canvas
  canvas.cd(counter)
  hist.Draw()

raw_input("Press Enter to continue...")


#
# Fraction of reco hits that are "good"
#

numRecoHits = rh.getFromFile(rootFiles['Reco hits'],'RecoHits/h_totalRecoHits').GetMean()
numGoodRecoHits = rh.getFromFile(rootFiles['Good reco hits'],'RecoHits/h_totalRecoHits').GetMean()

fractionGood = float(numGoodRecoHits) / float(numRecoHits) if len(numRecoHits)>0 else 0.
print 'Fraction reco hits that are good =',(fractionGood*100.)

