import os
import argparse
import RootHelper as rh

#Files to read
inputRootDir = '/unix/muons/g-2/scratch/tom/sim/gm2Dev_v6_01_00_testbeam_merge/data/sim/'
inputFileName = 'mtestRecoAnalysis_strawEfficiencyPlots.root'
efficiencyScanFiles = dict()
efficiencyScanFiles[0.25] = inputRootDir + 'strawEff25/' + inputFileName

#Loop over files
for efficiency, rootFileName in efficiencyScanFiles.iteritems():

  #Open input file
  rootFile = rh.openFile(rootFileName)

  #Get num digits in island histo
  h_numDigitsInIsland = rh.getFromFile(rootFile,'StrawEfficiency/Islands/h_numDigitsInIsland')

'''
#Draw it
g_doubletDriftTimes.SetTitle('Drift times in V layer doublet straw pairs (t0 from U layer doublet)')
#g_doubletDriftTimes.SetStats(False)
g_doubletDriftTimes.GetXaxis().SetTitle('Drift time (straw 0) [ns]')
g_doubletDriftTimes.GetYaxis().SetTitle('Drift time (straw 1) [ns]')
g_doubletDriftTimes.GetYaxis().SetTitleOffset(1.2)
g_doubletDriftTimes.GetXaxis().SetRangeUser(-10.,60.)
g_doubletDriftTimes.GetYaxis().SetRangeUser(-10.,60.)
g_doubletDriftTimes.SetMarkerStyle(7)
g_doubletDriftTimes.Draw("AP")
raw_input("Press Enter to continue...")


#
# Doublet drift time residuals
#

#Book histo
h_residuals = TH1F('h_residuals','Drift time residuals to fit [ns]', 100, -50., 50.)
h_residuals.GetXaxis().SetTitle('Drift time residual to fit [ns]')
h_residuals.GetYaxis().SetTitle('Counts')
h_residuals.GetYaxis().SetTitleOffset(1.2)

#Get residuals for all points on graph and fill histo
for i in range(0, g_doubletDriftTimes.GetN() ) :

  #Calculate residual
  driftTime0 = Double(0)
  driftTime1 = Double(0)
  g_doubletDriftTimes.GetPoint(i,driftTime0,driftTime1)
  residual = driftTime1 - ( slope*driftTime0 + intercept );
          
  #Fill histo
  h_residuals.Fill(residual)

#Draw it
'''

h_numDigitsInIsland.Draw()
raw_input("Press Enter to continue...")

