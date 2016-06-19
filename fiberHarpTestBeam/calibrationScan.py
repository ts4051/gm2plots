#Compare calibration scan results in different fibers

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TLegend
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./fiberHarpCalibrationPlots.root", \
                    help='Input ROOT file containing plots from FiberHarpCalibrationScan module', dest='inputFile')
args = parser.parse_args()

#Open input file
rootFile = rh.openFile(args.inputFile)
if not rootFile : sys.exit(-1)

gStyle.SetOptStat(0)

#Prepare multi-graphs
mg_x_amplitude = TMultiGraph()
leg_x_amplitude = TLegend(0.4,0.6,0.7,0.8)

mg_x_area = TMultiGraph()
leg_x_area = TLegend(0.4,0.6,0.7,0.8)

#
# Loop over fibers
#

for i_fiber in range(0,7) :

  fiberNum = i_fiber + 1

  fiberRootDirName = "harp_calibration_scan/fiber%i" % (fiberNum)

  #Get area plots
  g_x_area = rh.getFromFile(rootFile,fiberRootDirName+'/g_x_area')
  g_x_area.SetMarkerStyle(8)
  g_x_area.SetMarkerSize(1)
  g_x_area.SetMarkerColor(i_fiber+1)
  g_x_area.SetLineColor(i_fiber+1)
  mg_x_area.Add(g_x_area)
  leg_x_area.AddEntry(g_x_area, "Fiber %i" % fiberNum, "l" )

  #Get amplitude plots
  g_x_amplitude = rh.getFromFile(rootFile,fiberRootDirName+'/g_x_amplitude')
  g_x_amplitude.SetMarkerStyle(8)
  g_x_amplitude.SetMarkerSize(1)
  g_x_amplitude.SetMarkerColor(i_fiber+1)
  g_x_amplitude.SetLineColor(i_fiber+1)
  mg_x_amplitude.Add(g_x_amplitude)
  leg_x_amplitude.AddEntry(g_x_amplitude, "Fiber %i" % fiberNum, "l" )


#
# Draw the final multigraphs
#

mg_x_area.Draw("APL") #Draw once to populate axes
mg_x_area.GetXaxis().SetTitle( "Table x position [mm]" )
mg_x_area.GetYaxis().SetTitle( "Area" )
mg_x_area.GetYaxis().SetTitleOffset(1.2)
mg_x_area.GetYaxis().SetTitleOffset(1.5)
mg_x_area.SetTitle( "Mean fiber ampltiude vs table x position" )
mg_x_area.Draw("APL")
leg_x_area.SetFillStyle(0);
leg_x_area.SetBorderSize(0);
leg_x_area.Draw();
raw_input("Press Enter to continue...")

mg_x_amplitude.Draw("APL") #Draw once to populate axes
mg_x_amplitude.GetXaxis().SetTitle( "Table x position [mm]" )
mg_x_amplitude.GetYaxis().SetTitle( "Amplitude" )
mg_x_amplitude.GetYaxis().SetTitleOffset(1.2)
mg_x_amplitude.GetYaxis().SetTitleOffset(1.5)
mg_x_amplitude.SetTitle( "Mean fiber ampltiude vs table x position" )
mg_x_amplitude.Draw("APL")
leg_x_amplitude.SetFillStyle(0);
leg_x_amplitude.SetBorderSize(0);
leg_x_amplitude.Draw();
raw_input("Press Enter to continue...")

