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
  leg = TLegend(0.15,0.3,0.45,0.4)

  rootFiles = dict()
  h_efficiency = dict()

  i = 0
  for f in filePaths :

    rootFiles[f] = rh.openFile(f)
    h_efficiency[f] = rh.getFromFile(rootFiles[f],"h_dcaTriggers").Clone("h_efficiency%i"%i)
    h_efficiency[f].Divide(rh.getFromFile(rootFiles[f],"h_dcaTracks"))
    h_efficiency[f].Scale(100.)
    h_efficiency[f].SetTitle(";Track DCA to wire [mm];Efficiency [%]")
    h_efficiency[f].SetLineStyle(i+1)
    h_efficiency[f].SetLineColor(kBlue if i == 0 else kRed)
    h_efficiency[f].SetLineWidth(2)
    h_efficiency[f].GetYaxis().SetTitleOffset(1.3)
    h_efficiency[f].GetYaxis().SetRangeUser(0.,110.)
    h_efficiency[f].Draw( ("" if i == 0 else "same ") + "hist")

    legString = "%i V" % ( 1500 if i==0 else 1800 )
    leg.AddEntry(h_efficiency[f], legString, "l" )

    i += 1

  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  leg.Draw()

  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);

  canvas.Draw()
  canvas.SaveAs("./GarfieldEfficiencyMTest"+".eps")

  print "Done"

