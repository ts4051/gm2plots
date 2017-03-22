#TODO

from ROOT import TFile, gROOT, TCanvas, TPad, gStyle, TGraph, TH1F, TMultiGraph, TAxis, TGaxis, Double, kRed, kGreen, kBlue, kBlack, TEfficiency, TEllipse, TLegend, TH2F
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./truthPlots.root", help='Input ROOT file containing plots from StrawOccupancyPlots module', dest='inputFile')
parser.add_argument('-p','--pause-for-plots', action='store_true', help='Pause to allow user to look at each plot', dest='pauseForPlots')
parser.add_argument('-o','--output-dir', type=str, required=False, default="./", help='Output directory for images', dest='outputDir')
args = parser.parse_args()

#Check output directory exists
if not os.path.isdir(args.outputDir) :
  print "ERROR: Output directory does not exist : [%s]" % (args.outputDir)
  sys.exit(-1)

#Open input file
rootFile = rh.openFile(args.inputFile)

#
# Simple helper functions
#

#TODO REMOVE
'''
h1 = TH2F("h1","",10,0.,10.,10,0.,10.)
h1.Fill(5,5)
h1.Fill(5,5)
h1.Fill(1,1)
h1.Draw("COLZ")
raw_input("Press Enter to continue...")


h2 = TH2F("h1","",10,0.,10.,10,0.,10.)
h2.Fill(5,5)
h2.Fill(7,7)
h2.Draw("COLZ")
raw_input("Press Enter to continue...")

h1.Add(h2)
h1.Draw("COLZ")
raw_input("Press Enter to continue...")
'''
#
# Plot straw hit heat map (decay e+ only)
#

gStyle.SetOptStat(0)

canvas = TCanvas("canvas","",1000,600)

#Sum all trackers and average
h_numHitsInFillHeatMap = rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInFillHeatMap_station0").Clone("h1")
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInFillHeatMap_station12") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInFillHeatMap_station18") )
#h_numHitsInFillHeatMap.Scale( 1./3. )
h_numHitsInFillHeatMap.SetTitle("")
h_numHitsInFillHeatMap.GetXaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.GetYaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.Draw()

canvas.SetTopMargin(0.05);
canvas.SetLeftMargin(0.08);
canvas.SetRightMargin(0.1);
canvas.Draw()

canvas.SaveAs(args.outputDir+"/"+"StrawOccupancyHeatMapPrimaryDecayPositrons.eps")
if args.pauseForPlots : raw_input("Press Enter to continue...")


#
# Plot straw hit heat map (charged secondaries)
#

gStyle.SetOptStat(0)

canvas = TCanvas("canvas","",1000,600)

#Sum all trackers and average
h_numHitsInFillHeatMap = rh.getFromFile(rootFile,"straw_occupancy/secondary_e+e-/h_numHitsInFillHeatMap_station0").Clone("h2")
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_e+e-/h_numHitsInFillHeatMap_station12") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_e+e-/h_numHitsInFillHeatMap_station18") )
#h_numHitsInFillHeatMap.Scale( 1./3. )
h_numHitsInFillHeatMap.SetTitle("")
h_numHitsInFillHeatMap.GetXaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.GetYaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.Draw()

canvas.SetTopMargin(0.05);
canvas.SetLeftMargin(0.08);
canvas.SetRightMargin(0.1);
canvas.Draw()

canvas.SaveAs(args.outputDir+"/"+"StrawOccupancyHeatMapChargedSecondaries.eps")
if args.pauseForPlots : raw_input("Press Enter to continue...")

#
# Plot straw hit heat map (photons)
#

gStyle.SetOptStat(0)

canvas = TCanvas("canvas","",1000,600)

#Sum all trackers and average
h_numHitsInFillHeatMap = rh.getFromFile(rootFile,"straw_occupancy/secondary_photon/h_numHitsInFillHeatMap_station0").Clone("h3")
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_photon/h_numHitsInFillHeatMap_station12") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_photon/h_numHitsInFillHeatMap_station18") )
#h_numHitsInFillHeatMap.Scale( 1./3. )
h_numHitsInFillHeatMap.SetTitle("")
h_numHitsInFillHeatMap.GetXaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.GetYaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.Draw()

canvas.SetTopMargin(0.05);
canvas.SetLeftMargin(0.08);
canvas.SetRightMargin(0.1);
canvas.Draw()

canvas.SaveAs(args.outputDir+"/"+"StrawOccupancyHeatMapSecondaryPhotons.eps")
if args.pauseForPlots : raw_input("Press Enter to continue...")


#
# Plot straw hit heat map (all particles)
#

gStyle.SetOptStat(0)

canvas = TCanvas("canvas","",1000,600)

#Sum all trackers and average
h_numHitsInFillHeatMap = rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInFillHeatMap_station0").Clone("h4")
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInFillHeatMap_station12") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInFillHeatMap_station18") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_e+e-/h_numHitsInFillHeatMap_station0") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_e+e-/h_numHitsInFillHeatMap_station12") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_e+e-/h_numHitsInFillHeatMap_station18") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_photon/h_numHitsInFillHeatMap_station0") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_photon/h_numHitsInFillHeatMap_station12") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_photon/h_numHitsInFillHeatMap_station18") )
#h_numHitsInFillHeatMap.Scale( 1./3. )
h_numHitsInFillHeatMap.SetTitle("")
h_numHitsInFillHeatMap.GetXaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.GetYaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.Draw()

canvas.SetTopMargin(0.05);
canvas.SetLeftMargin(0.08);
canvas.SetRightMargin(0.1);
canvas.Draw()

canvas.SaveAs(args.outputDir+"/"+"StrawOccupancyHeatMapAllParticles.eps")
if args.pauseForPlots : raw_input("Press Enter to continue...")


#
# Plot straw hit heat map (all charged particle)
#

#TODO Add muons once lost muons are included

gStyle.SetOptStat(0)

canvas = TCanvas("canvas","",1000,600)

#Sum all trackers and average
h_numHitsInFillHeatMap = rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInFillHeatMap_station0").Clone("h5")
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInFillHeatMap_station12") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInFillHeatMap_station18") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_e+e-/h_numHitsInFillHeatMap_station0") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_e+e-/h_numHitsInFillHeatMap_station12") )
h_numHitsInFillHeatMap.Add( rh.getFromFile(rootFile,"straw_occupancy/secondary_e+e-/h_numHitsInFillHeatMap_station18") )
#h_numHitsInFillHeatMap.Scale( 1./3. )
h_numHitsInFillHeatMap.SetTitle("")
h_numHitsInFillHeatMap.GetXaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.GetYaxis().SetTitleOffset(1.1)
h_numHitsInFillHeatMap.Draw()

canvas.SetTopMargin(0.05);
canvas.SetLeftMargin(0.08);
canvas.SetRightMargin(0.1);
canvas.Draw()

canvas.SaveAs(args.outputDir+"/"+"StrawOccupancyHeatMapAllChargedParticles.eps")
if args.pauseForPlots : raw_input("Press Enter to continue...")


#
# Plot num hits in straws and TDCs per fill
#

'''

gStyle.SetOptStat(111111)

canvas = TCanvas("canvas","",700,600)

h_numHitsInStrawInAFill = rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInStrawInAFill")
h_numHitsInStrawInAFill.SetTitle(";Num hits in straw in fill")
h_numHitsInStrawInAFill.SetLineColor(kBlue)
h_numHitsInStrawInAFill.Draw()

canvas.SetTopMargin(0.05);
canvas.SetLeftMargin(0.1);
canvas.SetRightMargin(0.08);
canvas.Draw()

canvas.SaveAs(args.outputDir+"/"+"StrawOccupancy.eps")
if args.pauseForPlots : raw_input("Press Enter to continue...")


gStyle.SetOptStat(111111)

canvas = TCanvas("canvas","",700,600)

h_numHitsInTDCInFill = rh.getFromFile(rootFile,"straw_occupancy/primary_e+/h_numHitsInTDCInFill")
h_numHitsInTDCInFill.SetTitle(";Num hits in TDC in fill")
h_numHitsInTDCInFill.SetLineColor(kRed)
h_numHitsInTDCInFill.Draw()

canvas.SetTopMargin(0.05);
canvas.SetLeftMargin(0.1);
canvas.SetRightMargin(0.08);
canvas.Draw()

canvas.SaveAs(args.outputDir+"/"+"TDCOccupancy.eps")
if args.pauseForPlots : raw_input("Press Enter to continue...")

'''
