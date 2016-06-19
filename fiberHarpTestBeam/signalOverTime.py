#Compare calibration scan results in different fibers

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TLegend
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./fiberHarpSignalOverTimePlots.root", \
                    help='Input ROOT file containing plots from FiberHarpSignalOverTime module', dest='inputFile')
args = parser.parse_args()

#Open input file
rootFile = rh.openFile(args.inputFile)
if not rootFile : sys.exit(-1)

gStyle.SetOptStat(0)

#Prepare multi-graphs
mg_run_amplitude = TMultiGraph()
leg_run_amplitude = TLegend(0.4,0.6,0.7,0.8)

mg_run_area = TMultiGraph()
leg_run_area = TLegend(0.4,0.6,0.7,0.8)

#
# Loop over fibers
#

for i_fiber in range(0,7) :

  fiberNum = i_fiber + 1

  fiberRootDirName = "harp_signal_over_time/fiber%i" % (fiberNum)

  #Get area plots
  g_run_area = rh.getFromFile(rootFile,fiberRootDirName+'/g_run_area')
  g_run_area.SetMarkerStyle(8)
  g_run_area.SetMarkerSize(1)
  g_run_area.SetMarkerColor(i_fiber+1)
  g_run_area.SetLineColor(i_fiber+1)
  mg_run_area.Add(g_run_area)
  leg_run_area.AddEntry(g_run_area, "Fiber %i" % fiberNum, "l" )

  #Get amplitude plots
  g_run_amplitude = rh.getFromFile(rootFile,fiberRootDirName+'/g_run_amplitude')
  g_run_amplitude.SetMarkerStyle(8)
  g_run_amplitude.SetMarkerSize(1)
  g_run_amplitude.SetMarkerColor(i_fiber+1)
  g_run_amplitude.SetLineColor(i_fiber+1)
  mg_run_amplitude.Add(g_run_amplitude)
  leg_run_amplitude.AddEntry(g_run_amplitude, "Fiber %i" % fiberNum, "l" )


#
# Draw the final multigraphs
#

mg_run_area.Draw("APL") #Draw once to populate axes
mg_run_area.GetXaxis().SetTitle( "Run num" )
mg_run_area.GetYaxis().SetTitle( "Area" )
mg_run_area.GetYaxis().SetTitleOffset(1.2)
mg_run_area.GetYaxis().SetTitleOffset(1.5)
mg_run_area.SetTitle( "Mean fiber ampltiude vs table x position" )
mg_run_area.Draw("APL")
leg_run_area.SetFillStyle(0);
leg_run_area.SetBorderSize(0);
leg_run_area.Draw();
raw_input("Press Enter to continue...")

mg_run_amplitude.Draw("APL") #Draw once to populate axes
mg_run_amplitude.GetXaxis().SetTitle( "Run num" )
mg_run_amplitude.GetYaxis().SetTitle( "Amplitude" )
mg_run_amplitude.GetYaxis().SetTitleOffset(1.2)
mg_run_amplitude.GetYaxis().SetTitleOffset(1.5)
mg_run_amplitude.SetTitle( "Mean fiber ampltiude vs table x position" )
mg_run_amplitude.Draw("APL")
leg_run_amplitude.SetFillStyle(0);
leg_run_amplitude.SetBorderSize(0);
leg_run_amplitude.Draw();
raw_input("Press Enter to continue...")

