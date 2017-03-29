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

  filePaths = [ "/Users/stuttard/physics/gm2/software/offline/gm2plots/garfield/runPlots_mtest-lowgain-1500V_10kevts.root"  , "/Users/stuttard/physics/gm2/software/offline/gm2plots/garfield/runPlots_mtest_10kevts.root" ]

  gStyle.SetOptStat(0) #111111)

  canvas = TCanvas("canvas","",800,600)
  leg = TLegend(0.15,0.8,0.45,0.9)

  rootFiles = dict()
  h_driftTimes = dict()

  i = 0
  for f in filePaths :

    rootFiles[f] = rh.openFile(f)
    h_driftTimes[f] = rh.getFromFile(rootFiles[f],"h_firstCrossingTime").Clone("h_driftTimes%i"%i)
    h_driftTimes[f].Rebin(2)
    h_driftTimes[f].Scale( 1./float(h_driftTimes[f].GetMaximum()) )
#    h_driftTimes[f].Scale( 1./float(h_driftTimes[f].GetEntries()) )
    h_driftTimes[f].SetTitle(";Drift time [ns];Counts [arb. units]")
    h_driftTimes[f].GetYaxis().SetTitleOffset(0.8)
    h_driftTimes[f].GetYaxis().SetLabelSize(0.)
    h_driftTimes[f].SetLineStyle(0)
    h_driftTimes[f].SetLineColor(kBlue if i == 0 else kRed)
    h_driftTimes[f].SetLineWidth(2)
    #h_driftTimes.GetXaxis().SetRangeUser(-1500.,1500.)
    h_driftTimes[f].Draw( ("" if i == 0 else "same ") + "hist")
    legString = "%i V" % ( 1500 if i==0 else 1800 )
    leg.AddEntry(h_driftTimes[f], legString, "l" )

    i += 1

  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  leg.Draw()

  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);

  canvas.Draw()
  canvas.SaveAs("./GarfieldDriftTimesMTest"+".eps")

  print "Done"

