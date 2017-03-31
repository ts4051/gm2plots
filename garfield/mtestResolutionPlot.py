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
  h_recoDCAResiduals = dict()

  i = 0
  for f in filePaths :

    rootFiles[f] = rh.openFile(f)
    h_recoDCAResiduals[f] = rh.getFromFile(rootFiles[f],"h_recoDCAResiduals").Clone("h_recoDCAResiduals%i"%i)
    h_recoDCAResiduals[f].Scale( 1./float(h_recoDCAResiduals[f].GetMaximum()) )
    h_recoDCAResiduals[f].SetTitle(";Reconstructed - true track DCA to wire [um]; Counts [arb. units]")
    h_recoDCAResiduals[f].GetYaxis().SetTitleOffset(0.8)
    h_recoDCAResiduals[f].GetYaxis().SetLabelSize(0.)
    h_recoDCAResiduals[f].SetLineStyle(i+1)
    h_recoDCAResiduals[f].SetLineColor(kBlue if i == 0 else kRed)
    h_recoDCAResiduals[f].SetLineWidth(2)
    #h_recoDCAResiduals.GetXaxis().SetRangeUser(-1500.,1500.)
    h_recoDCAResiduals[f].Draw( ("" if i == 0 else "same ") + "hist")

    '''
    f_residuals = TF1("f_recoDCAResiduals%i"%i, "gaus", -1.5e3, 1.5e3);
    h_recoDCAResiduals.Fit("f_recoDCAResiduals%i"%i,"R")
    fitSigma = f_residuals.GetParameter(2)
    '''
    legString = "%i V : RMS = %0.3g [um]" % ( 1500 if i==0 else 1800 , h_recoDCAResiduals[f].GetRMS() )
    leg.AddEntry(h_recoDCAResiduals[f], legString, "l" )

    i += 1

  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  leg.Draw()

  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);

  canvas.Draw()
  canvas.SaveAs("./GarfieldRecoDCAResidualsMTest"+".eps")

  print "Done"

