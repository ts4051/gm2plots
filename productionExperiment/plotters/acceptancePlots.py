#TODO

from ROOT import TFile, gROOT, TCanvas, TPad, gStyle, TGraph, TH1F, TMultiGraph, TAxis, TGaxis, Double, kRed, kGreen, kBlue, kBlack
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./truthPlots.root", help='Input ROOT file containing plots from StrawAndCaloTruthPlots module', dest='inputFile')
args = parser.parse_args()

#Open input file
rootFile = rh.openFile(args.inputFile)


#
# Functions for plotting ratio of two histograms
#

def plotRatioOfTwoHistos(numeratorHistoName,denominatorHistoName,title,xtitle,addScaledPlot) :

  # Get the two histograms
  hn = rh.getFromFile(rootFile,numeratorHistoName)
  hd = rh.getFromFile(rootFile,denominatorHistoName)

  # Find which has the largest value
  numeratorHistoHasLargestValue = True if hn.GetMaximum() > hd.GetMaximum() else False

  # Normalise
  #hn.Scale( 1. / hn.Integral() )
  #hd.Scale( 1. / hd.Integral() )

  # Define the Canvas
  c = TCanvas("c", "canvas", 800, 800)

  # Upper plot will be in topPad
  topPad = TPad("topPad", "topPad", 0, 0.3, 1, 1.0)
  topPad.SetBottomMargin(0.04) # Upper and lower plot are joined
  topPad.SetGridx()         # Vertical grid
  topPad.Draw()             # Draw the upper pad: topPad
  topPad.cd()               # topPad becomes the current pad
  hn.SetStats(0)          # No statistics on upper plot

  # Draw histo with largest value first (to get correct y axis range), then overlay other
  if numeratorHistoHasLargestValue : 
    hn.SetTitle(title)
    hn.Draw()               # Draw hn
    hd.Draw("same")         # Draw hd on top of hn
  else :
    hd.SetTitle(title)
    hd.Draw()               # Draw hd
    hn.Draw("same")         # Draw hn on top of hd

  # Draw a scaled version of the smaller histo for ease of viewer
  if addScaledPlot :
    hs = hd.Clone("hs") if numeratorHistoHasLargestValue else hn.Clone("hs")
    maxBin = hd.GetMaximumBin() if numeratorHistoHasLargestValue else hn.GetMaximumBin()
    scaleFactor = hn.GetBinContent(maxBin)/hd.GetBinContent(maxBin) if numeratorHistoHasLargestValue else hd.GetBinContent(maxBin)/hn.GetBinContent(maxBin)
    hs.Scale(scaleFactor)
    hs.SetStats(0)
    hs.Draw("same")

  # Do not draw the Y axis label on the upper plot and redraw a small
  # axis instead, in order to avoid the first label (0) to be clipped.

  # lower plot will be in pad
  c.cd()          # Go back to the main canvas before defining bottomPad
  bottomPad = TPad("bottomPad", "bottomPad", 0, 0.05, 1, 0.3)
  bottomPad.SetBottomMargin(0.25)
  bottomPad.SetGridx() # vertical grid
  bottomPad.Draw()
  bottomPad.cd()       # bottomPad becomes the current pad

  # Define the ratio plot
  hr = hn.Clone("hr")
  hr.SetLineColor(kBlack)
  #hr.SetMinimum(0.8)  # Define Y ..
  #hr.SetMaximum(1.35) # .. range
  hr.Sumw2()
  hr.SetStats(0)      # No statistics on lower plot
  hr.Divide(hd)
  hr.Scale(100.)      # Ratio -> percentage
  hr.SetMarkerStyle(21)
  hr.Draw("ep")       # Draw the ratio plot

  # hn settings
  hn.SetLineColor(kBlue+1)
  hn.SetLineWidth(2)

  # X axis hn plot settings
  hn.GetXaxis().SetTitleSize(0)
  hn.GetXaxis().SetLabelSize(0)

  # Y axis hn plot settings
  hn.GetYaxis().SetTitleSize(20)
  hn.GetYaxis().SetTitleFont(43)
  hn.GetYaxis().SetTitleOffset(1.55)

  # hd settings
  hd.SetLineColor(kRed)
  hd.SetLineWidth(2)

  # hs settings
  if addScaledPlot :
    if numeratorHistoHasLargestValue : hs.SetLineColor(kRed)
    else : hs.SetLineColor(kBlue+1)
    hs.SetLineWidth(2)
    hs.SetLineStyle(7)

  # Ratio plot (hr) settings
  hr.SetTitle("") # Remove the ratio title
  hr.GetXaxis().SetTitle(xtitle)

  # Y axis ratio plot settings
  hr.GetYaxis().SetTitle("ratio (%)")
  hr.GetYaxis().SetNdivisions(505)
  hr.GetYaxis().SetTitleSize(20)
  hr.GetYaxis().SetTitleFont(43)
  hr.GetYaxis().SetTitleOffset(1.55)
  hr.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  hr.GetYaxis().SetLabelSize(15)

  # X axis ratio plot settings
  hr.GetXaxis().SetTitleSize(20)
  hr.GetXaxis().SetTitleFont(43)
  hr.GetXaxis().SetTitleOffset(4.)
  hr.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  hr.GetXaxis().SetLabelSize(15)

  # Set ratio plot x axis range
  minNonZeroBinContent = 1.e99
  for i_bin in range(1,hr.GetXaxis().GetNbins()+1) :
    binContent = hr.GetBinContent(i_bin)
    if binContent > 0. :
      minNonZeroBinContent = min(binContent,minNonZeroBinContent) 
  hr.GetYaxis().SetRangeUser(minNonZeroBinContent*0.6,hr.GetMaximum()*1.4)

  # wait so user can see the plot
  raw_input("Press Enter to continue...")

#TODO
'''
def plotRatioOfTwo2DHistos(numeratorHistoName,denominatorHistoName,title,xtitle,addScaledPlot) :

  # Get the two histograms
  hn = rh.getFromFile(rootFile,numeratorHistoName)
  hd = rh.getFromFile(rootFile,denominatorHistoName)

  # Find which has the largest value
  numeratorHistoHasLargestValue = True if hn.GetMaximum() > hd.GetMaximum() else False

  # Normalise
  #hn.Scale( 1. / hn.Integral() )
  #hd.Scale( 1. / hd.Integral() )

  # Define the Canvas
  c = TCanvas("c", "canvas", 800, 800)

  # Upper plot will be in topPad
  topPad = TPad("topPad", "topPad", 0, 0.3, 1, 1.0)
  topPad.SetBottomMargin(0.04) # Upper and lower plot are joined
  topPad.SetGridx()         # Vertical grid
  topPad.Draw()             # Draw the upper pad: topPad
  topPad.cd()               # topPad becomes the current pad
  hn.SetStats(0)          # No statistics on upper plot

  # Draw histo with largest value first (to get correct y axis range), then overlay other
  if numeratorHistoHasLargestValue : 
    hn.SetTitle(title)
    hn.Draw()               # Draw hn
    hd.Draw("same")         # Draw hd on top of hn
  else :
    hd.SetTitle(title)
    hd.Draw()               # Draw hd
    hn.Draw("same")         # Draw hn on top of hd

  # Draw a scaled version of the smaller histo for ease of viewer
  if addScaledPlot :
    hs = hd.Clone("hs") if numeratorHistoHasLargestValue else hn.Clone("hs")
    maxBin = hd.GetMaximumBin() if numeratorHistoHasLargestValue else hn.GetMaximumBin()
    scaleFactor = hn.GetBinContent(maxBin)/hd.GetBinContent(maxBin) if numeratorHistoHasLargestValue else hd.GetBinContent(maxBin)/hn.GetBinContent(maxBin)
    hs.Scale(scaleFactor)
    hs.SetStats(0)
    hs.Draw("same")

  # Do not draw the Y axis label on the upper plot and redraw a small
  # axis instead, in order to avoid the first label (0) to be clipped.

  # lower plot will be in pad
  c.cd()          # Go back to the main canvas before defining bottomPad
  bottomPad = TPad("bottomPad", "bottomPad", 0, 0.05, 1, 0.3)
  bottomPad.SetBottomMargin(0.25)
  bottomPad.SetGridx() # vertical grid
  bottomPad.Draw()
  bottomPad.cd()       # bottomPad becomes the current pad

  # Define the ratio plot
  hr = hn.Clone("hr")
  hr.SetLineColor(kBlack)
  #hr.SetMinimum(0.8)  # Define Y ..
  #hr.SetMaximum(1.35) # .. range
  hr.Sumw2()
  hr.SetStats(0)      # No statistics on lower plot
  hr.Divide(hd)
  hr.Scale(100.)      # Ratio -> percentage
  hr.SetMarkerStyle(21)
  hr.Draw("ep")       # Draw the ratio plot

  # hn settings
  hn.SetLineColor(kBlue+1)
  hn.SetLineWidth(2)

  # X axis hn plot settings
  hn.GetXaxis().SetTitleSize(0)
  hn.GetXaxis().SetLabelSize(0)

  # Y axis hn plot settings
  hn.GetYaxis().SetTitleSize(20)
  hn.GetYaxis().SetTitleFont(43)
  hn.GetYaxis().SetTitleOffset(1.55)

  # hd settings
  hd.SetLineColor(kRed)
  hd.SetLineWidth(2)

  # hs settings
  if addScaledPlot :
    if numeratorHistoHasLargestValue : hs.SetLineColor(kRed)
    else : hs.SetLineColor(kBlue+1)
    hs.SetLineWidth(2)
    hs.SetLineStyle(7)

  # Ratio plot (hr) settings
  hr.SetTitle("") # Remove the ratio title
  hr.GetXaxis().SetTitle(xtitle)

  # Y axis ratio plot settings
  hr.GetYaxis().SetTitle("ratio (%)")
  hr.GetYaxis().SetNdivisions(505)
  hr.GetYaxis().SetTitleSize(20)
  hr.GetYaxis().SetTitleFont(43)
  hr.GetYaxis().SetTitleOffset(1.55)
  hr.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  hr.GetYaxis().SetLabelSize(15)

  # X axis ratio plot settings
  hr.GetXaxis().SetTitleSize(20)
  hr.GetXaxis().SetTitleFont(43)
  hr.GetXaxis().SetTitleOffset(4.)
  hr.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  hr.GetXaxis().SetLabelSize(15)

  # Set ratio plot x axis range
  minNonZeroBinContent = 1.e99 #Start with something massive
  for i_bin in range(1,hr.GetXaxis().GetNbins()+1) :
    binContent = hr.GetBinContent(i_bin)
    if binContent > 0. :
      minNonZeroBinContent = min(binContent,minNonZeroBinContent) 
  hr.GetYaxis().SetRangeUser(minNonZeroBinContent*0.6,hr.GetMaximum()*1.4)

  # wait so user can see the plot
  raw_input("Press Enter to continue...")
'''

#
# Plot ratios for all desired histo combinations
#

gStyle.SetOptStat(0)

#Vertex radial pos
plotRatioOfTwoHistos("straw_calo_truth/primary_e+/tracker/trackable/h_vertexDeltaR","trajectories/primary_e+/h_birthDeltaR","Trackers","Vertex r (relative to magic r) [mm]",True)
plotRatioOfTwoHistos("straw_calo_truth/primary_e+/calo/h_vertexDeltaR","trajectories/primary_e+/h_birthDeltaR","Calorimeters","Vertex r (relative to magic r) [mm]",True)

#Vertex vertical pos
plotRatioOfTwoHistos("straw_calo_truth/primary_e+/tracker/trackable/h_vertexHeight","trajectories/primary_e+/h_birthY","Trackers","Vertex vertical pos [mm]",True)
plotRatioOfTwoHistos("straw_calo_truth/primary_e+/calo/h_vertexHeight","trajectories/primary_e+/h_birthY","Calorimeters","Vertex vertical pos [mm]",True)

#Vertex E
plotRatioOfTwoHistos("straw_calo_truth/primary_e+/tracker/trackable/h_vertexE","trajectories/primary_e+/h_birthE","Trackers","Vertex E [MeV]",True)
plotRatioOfTwoHistos("straw_calo_truth/primary_e+/calo/h_vertexE","trajectories/primary_e+/h_birthE","Calorimeters","Vertex E [MeV]",False)


