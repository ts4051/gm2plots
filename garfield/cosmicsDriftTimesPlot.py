#Grab plots from runPlots.root and clean up, combine, etc for thesis
#Tom Stuttard

from ROOT import TFile, gROOT, TH1F, TH2F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree, TProfile, TCanvas, TF1, TLegend, kBlack
import os, argparse, math, sys
import RootHelper as rh
import garfieldHelper as gh


#
# Main function
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)


  #
  # Resolution
  #

  filePaths = [ \
    "/Users/stuttard/physics/gm2/software/offline/gm2plots/garfield/runPlots_cosmics_10kevts.root"  , \
    "/Users/stuttard/physics/gm2/software/offline/gm2plots/garfield/runPlots_cosmics-0.1GeV_5kevts.root" , \
    "/Users/stuttard/physics/gm2/software/offline/gm2plots/garfield/runPlots_cosmics-10GeV_5kevts.root"  \
    ]

  gStyle.SetOptStat(0) #111111)

  canvas = TCanvas("canvas","",800,600)

  rootFiles = dict()

  i = 0
  rootFiles[i] = rh.openFile(filePaths[i])
  h_driftTimes = rh.getFromFile(rootFiles[i],"h_firstCrossingTime").Clone("h_driftTimes%i"%i)
  i += 1
  while i < len(filePaths) :
    rootFiles[i] = rh.openFile(filePaths[i])
    h_driftTimes.Add( rh.getFromFile(rootFiles[i],"h_firstCrossingTime").Clone("h_driftTimes%i"%i) )
    i += 1

  h_driftTimes.Rebin(2)
#    h_driftTimes[f].Scale( 1./float(h_driftTimes[f].GetEntries()) )
  h_driftTimes.SetTitle(";Drift time [ns];Counts [arb. units]")
  h_driftTimes.GetYaxis().SetTitleOffset(0.8)
  h_driftTimes.GetYaxis().SetLabelSize(0.)
  h_driftTimes.SetLineStyle(0)
  h_driftTimes.SetLineColor(kRed)
  h_driftTimes.SetLineWidth(2)
  #h_driftTimes.GetXaxis().SetRangeUser(-1500.,1500.)
  h_driftTimes.Draw("hist")


  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);

  canvas.Draw()
  canvas.SaveAs("./GarfieldDriftTimesCosmics"+".eps")

  print "Done"

