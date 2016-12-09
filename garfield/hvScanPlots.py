#Plot straw performance vs wire voltage
#Tom Stuttard

from ROOT import TFile, gROOT, gDirectory, TH1F, TH2F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree, TProfile
import os, argparse, math, sys
import RootHelper as rh
import garfieldHelper as gh

#
# Main function
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #Get args
  parser = argparse.ArgumentParser(description='')
#  parser.add_argument('-i','--input-file', type=str, required=True, help='Input ROOT file', dest='inputFile')
  parser.add_argument('-p','--pause-for-plots', action='store_true', help='Pause to allow user to look at each plot', dest='pauseForPlots')
  args = parser.parse_args()

  #Input files list #TODO Make an arg
  '''
  inputFiles = [ \
#    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_3000V.root", \
#    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_2500V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1900V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1850V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1750V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1650V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1550V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1500V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1450V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1400V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1300V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1200V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_1000V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/src/RunGarfieldStrawModel_500V.root" \
  ]
  '''

  '''
  inputFiles = [ \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/old/RunGarfieldStrawModel_1000V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/old/RunGarfieldStrawModel_1100V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/old/RunGarfieldStrawModel_1200V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/old/RunGarfieldStrawModel_1300V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/old/RunGarfieldStrawModel_1400V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/old/RunGarfieldStrawModel_1500V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/old/RunGarfieldStrawModel_1600V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/old/RunGarfieldStrawModel_1700V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/old/RunGarfieldStrawModel_1800V.root" \
  ]
  '''

  
  inputFiles = [ \
#    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1000V.root", \
#    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1050V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1100V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1150V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1200V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1250V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1300V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1350V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1400V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1450V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1500V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1550V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1600V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1650V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1700V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1750V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/ethane/RunGarfieldStrawModel_1800V.root" \
  ]
  
  '''
  inputFiles = [ \
#    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1000V.root", \
#    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1050V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1100V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1150V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1200V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1250V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1300V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1350V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1400V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1450V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1500V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1550V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1600V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1650V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1700V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1750V.root", \
    "/unix/muons/g-2/scratch/tom/sim/garfield/gm2trackerdaq/garfield/c++/data/sr90HVScan/co2/RunGarfieldStrawModel_1800V.root" \
  ]
  '''



  #
  # Prepare plots
  #

  g_gain_vs_wireVoltage = TGraph() 
  g_numHits_vs_wireVoltage = TGraph() 
  g_hitEfficiency_vs_wireVoltage = TGraph() 

  #Init plotting
  gStyle.SetOptStat(111111)


  #
  # Loop over input files
  #

  i_file = 0 

  for inputFile in inputFiles :

    #Open input file
    print "\n+++ Opening %s\n" % (inputFile)
    rootFile = rh.openFile(inputFile)
    if not rootFile : sys.exit(-1)

    #Get run info tree
    t_runInfo = rh.getFromFile(rootFile,"Garfield/RunInfo")
    t_runInfo.GetEntry(0) #Only one entry

    #
    # Event loop
    #

    #Get event tree
    t_event = rh.getFromFile(rootFile,"Garfield/Events")

    #Get mean gain for this run
    tmpHistName = "h_tmp_%i" % (i_file)
    t_event.Draw("electronGain>>%s" % (tmpHistName) )
    gain = gDirectory.Get(tmpHistName).GetMean()

    #Plot gain vs HV
    g_gain_vs_wireVoltage.SetPoint( g_gain_vs_wireVoltage.GetN(), t_runInfo.wireVoltageV, gain )

    #Loop over events
    numHits = 0
    numEvents = t_event.GetEntries()
    for i_evt in range(0,numEvents) :

      #Step tree to current event
      t_event.GetEntry(i_evt)

      #Count hits #TODO multi hits?
      if len(t_event.thresholdCrossingTimes) > 0 : numHits += 1

    #Plot num hits vs HV
    g_numHits_vs_wireVoltage.SetPoint( g_numHits_vs_wireVoltage.GetN(), t_runInfo.wireVoltageV, numHits )
    hitEfficiency = 100. * float(numHits) / float(numEvents)
    g_hitEfficiency_vs_wireVoltage.SetPoint( g_hitEfficiency_vs_wireVoltage.GetN(), t_runInfo.wireVoltageV, hitEfficiency )

    i_file += 1

  print "+++ Done processing files"

  #
  # Draw plots
  # 

  if args.pauseForPlots : raw_input("Press Enter to continue...")

  g_gain_vs_wireVoltage.SetTitle(";HV [V];Gain") 
  g_gain_vs_wireVoltage.SetMarkerStyle(7)
  g_gain_vs_wireVoltage.Draw("AP") 
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  g_numHits_vs_wireVoltage.SetTitle(";HV [V];Num hits") 
  g_numHits_vs_wireVoltage.SetMarkerStyle(7)
  g_numHits_vs_wireVoltage.Draw("AP") 
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  g_hitEfficiency_vs_wireVoltage.SetTitle(";HV [V]; Efficiency [%]") 
  g_hitEfficiency_vs_wireVoltage.SetMarkerStyle(7)
  g_hitEfficiency_vs_wireVoltage.Draw("AP") 
  if args.pauseForPlots : raw_input("Press Enter to continue...")


  #
  # Write to file
  #

  outputFileName = "hvScanPlots.root"
  outputFile = TFile(outputFileName,"RECREATE")

  g_gain_vs_wireVoltage.SetName("g_gain_vs_wireVoltage")
  g_gain_vs_wireVoltage.Write()

  g_hitEfficiency_vs_wireVoltage.SetName("g_hitEfficiency_vs_wireVoltage")
  g_hitEfficiency_vs_wireVoltage.Write()

  outputFile.Close()

  print "+++ Done : Output file = %s" % (outputFileName)


