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

  filePath = "/Users/stuttard/physics/gm2/software/offline/gm2plots/garfield/runPlots_cosmics_5kevts.root"

  gStyle.SetOptStat(0) #111111)

  canvas = TCanvas("canvas","",800,600)

  rootFile = rh.openFile(filePath)

  h_driftTimes = rh.getFromFile(rootFile,"h_firstCrossingTime").Clone("h_driftTimes")
  h_driftTimes.Rebin(2)
#    h_driftTimes[f].Scale( 1./float(h_driftTimes[f].GetEntries()) )
  #h_driftTimes.SetTitle(";Drift time [ns];Counts [arb. units]")
  h_driftTimes.GetYaxis().SetTitleOffset(0.8)
  h_driftTimes.GetYaxis().SetLabelSize(0.)
  h_driftTimes.SetLineStyle(0)
  h_driftTimes.SetLineColor(kRed)
  h_driftTimes.SetLineWidth(2)
  #h_driftTimes.GetXaxis().SetRangeUser(-1500.,1500.)
  h_driftTimes.Draw("hist")


  h_driftTimesSmeared = rh.getFromFile(rootFile,"h_firstCrossingTimeSmeared").Clone("h_driftTimesSmeared")
  h_driftTimesSmeared.Rebin(2)
#    h_driftTimesSmeared[f].Scale( 1./float(h_driftTimes[f].GetEntries()) )
  h_driftTimesSmeared.SetTitle(";Drift time [ns];Counts [arb. units]")
  h_driftTimesSmeared.GetYaxis().SetTitleOffset(0.8)
  h_driftTimesSmeared.GetYaxis().SetLabelSize(0.)
  h_driftTimesSmeared.SetLineStyle(0)
  h_driftTimesSmeared.SetLineColor(kBlue)
  h_driftTimesSmeared.SetLineWidth(2)
  #h_driftTimesSmeared.GetXaxis().SetRangeUser(-1500.,1500.)
  h_driftTimesSmeared.Draw("hist same")

  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);

  canvas.Draw()
  canvas.SaveAs("./GarfieldDriftTimesCosmicsSmeared"+".eps")

  print "Done"

