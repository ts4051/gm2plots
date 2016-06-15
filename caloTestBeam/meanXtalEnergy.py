#Compare mean xtal E across multiple runs

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./meanEnergyPlots.root", help='Input ROOT file containing plots from MeanElectronE module', dest='inputFile')
args = parser.parse_args()

#Open input file
rootFile = rh.openFile(args.inputFile)
if not rootFile : sys.exit(-1)

gStyle.SetOptStat(0)


mg_electronMeanE = TMultiGraph()
mg_laserMeanE = TMultiGraph()


#
# Loop over xtals
#

for i_xtal in range(0,54) :

  xtalRootDirName = "mean_electron_energy/xtal_%02i" % (i_xtal)


  #
  # Get electron and laser E sum graphs
  #

  g_electronMeanE = rh.getFromFile(rootFile,xtalRootDirName+'/g_electronMeanE')
  g_electronMeanE.SetMarkerStyle(8)
  g_electronMeanE.SetMarkerSize(1)
  g_electronMeanE.SetMarkerColor(i_xtal+1)
  g_electronMeanE.SetLineColor(i_xtal+1)
  mg_electronMeanE.Add(g_electronMeanE)

  g_laserMeanE = rh.getFromFile(rootFile,xtalRootDirName+'/g_laserMeanE')
  g_laserMeanE.SetMarkerStyle(8)
  g_laserMeanE.SetMarkerColor(i_xtal+1)
  g_laserMeanE.SetLineColor(i_xtal+1)
  mg_laserMeanE .Add(g_laserMeanE)

  #Record num runs for later
  numRuns = g_laserMeanE.GetN()



#
# Correct e- E sum based on laser 
#

mg_correctedElectronMeanE = TMultiGraph()
g_correctedElectronMeanE = dict()

for i_xtal in range(0,54) :

  xtalRootDirName = "mean_electron_energy/xtal_%02i" % (i_xtal)
  g_electronMeanE = rh.getFromFile(rootFile,xtalRootDirName+'/g_electronMeanE')

  g_correctedElectronMeanE[i_xtal] = TGraph(g_electronMeanE.GetN())
  g_correctedElectronMeanE[i_xtal].SetName("g_correctedElectronMeanE_xtal%02i"%i_xtal)

  #Step through runs and make corrections (this xtal only)
  for i_point in range(0,g_electronMeanE.GetN()) :

    runNum = Double(0)
    electronMeanE = Double(0)
    g_electronMeanE.GetPoint(i_point,runNum,electronMeanE)

    laserMeanE = Double(0)
    g_laserMeanE.GetPoint(i_point,runNum,laserMeanE) #Same run num

    #Handle laser baseline calibration changes at certain runs
    laserBaseLineE = 0.
    if runNum >= 2894 and runNum <= 3048 : laserBaseLineE = 80725. #TODO per xtal
    elif runNum >= 3049 and runNum <= 9999 : laserBaseLineE = 10. #TODO
    else:
      print "No known calibration for run %i" % (runNum)
      sys.exit(-1)


    #TODO Do relative to first run after calibration instead
    #TODO Do relative to first run after calibration instead
    #TODO Do relative to first run after calibration instead
    #TODO Do relative to first run after calibration instead
    x = Double()
    laserBaseLineE = Double()
    g_laserMeanE.GetPoint(0,x,laserBaseLineE) #Don't change runNum variable
    #TODO Do relative to first run after calibration instead
    #TODO Do relative to first run after calibration instead
    #TODO Do relative to first run after calibration instead
    #TODO Do relative to first run after calibration instead



    #Determine laser gain correction relative to baseline for this run
    laserCorrection = float(laserMeanE) / float(laserBaseLineE) #TODO div 0 protection

    #Correct electron E by this factor
    correctedElectronMeanE =  electronMeanE / laserCorrection
    g_correctedElectronMeanE[i_xtal].SetPoint(i_point,runNum,correctedElectronMeanE)

    #Add corrected electron E sum to plot
    g_correctedElectronMeanE[i_xtal].SetMarkerStyle(8)
    g_correctedElectronMeanE[i_xtal].SetMarkerColor(i_xtal+1)
    g_correctedElectronMeanE[i_xtal].SetLineColor(i_xtal+1)
    mg_correctedElectronMeanE.Add(g_correctedElectronMeanE[i_xtal])


#
# Draw the final multigraphs
#

mg_electronMeanE.Draw("APL") #Draw once to populate axes
mg_electronMeanE.GetXaxis().SetTitle( "Run number" )
mg_electronMeanE.GetYaxis().SetTitle( "Mean electron xtal energy [photoelectrons]" )
mg_electronMeanE.GetYaxis().SetTitleOffset(1.2)
mg_electronMeanE.GetYaxis().SetTitleOffset(1.5)
mg_electronMeanE.SetTitle( "Mean electron energy in all xtals per run" )
mg_electronMeanE.Draw("APL")
raw_input("Press Enter to continue...")

mg_laserMeanE.Draw("APL") #Draw once to populate axes
mg_laserMeanE.GetXaxis().SetTitle( "Run number" )
mg_laserMeanE.GetYaxis().SetTitle( "Mean laser xtal energy [photoelectrons]" )
mg_laserMeanE.GetYaxis().SetTitleOffset(1.2)
mg_laserMeanE.GetYaxis().SetTitleOffset(1.5)
mg_laserMeanE.SetTitle( "Mean laser energy in all xtals per run" )
mg_laserMeanE.Draw("APL")
raw_input("Press Enter to continue...")

mg_correctedElectronMeanE.Draw("APL") #Draw once to populate axes
mg_correctedElectronMeanE.GetXaxis().SetTitle( "Run number" )
mg_correctedElectronMeanE.GetYaxis().SetTitle( "Corrected mean electron xtal energy [photoelectrons]" )
mg_correctedElectronMeanE.GetYaxis().SetTitleOffset(1.2)
mg_correctedElectronMeanE.GetYaxis().SetTitleOffset(1.5)
mg_correctedElectronMeanE.SetTitle( "Corrected mean electron energy in all xtals per run" )
mg_correctedElectronMeanE.Draw("APL")
raw_input("Press Enter to continue...")

g_correctedElectronClusterMeanE.GetXaxis().SetTitle( "Run number" )
g_correctedElectronClusterMeanE.GetYaxis().SetTitle( "Mean electron cluster energy using per xtal laser correction [photoelectrons]" )
g_correctedElectronClusterMeanE.GetYaxis().SetTitleOffset(1.2)
g_correctedElectronClusterMeanE.GetYaxis().SetTitleOffset(1.5)
g_correctedElectronClusterMeanE.SetMarkerStyle(8)
g_correctedElectronClusterMeanE.SetMarkerSize(1)
g_correctedElectronClusterMeanE.SetMarkerColor(kRed)
g_correctedElectronClusterMeanE.SetLineColor(kRed)
g_correctedElectronClusterMeanE.Draw("APL")
raw_input("Press Enter to continue...")

