#Grab plots from runPlots.root and clean up, combine, etc for thesis
#Tom Stuttard

from ROOT import TFile, gROOT, TH1F, TH2F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree, TProfile, TCanvas, TF1, TLegend
import os, argparse, math, sys
import RootHelper as rh
import garfieldHelper as gh


#
# Main function
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #Get args
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('-i','--input-file', type=str, required=True, help='Input ROOT file', dest='inputFile')
  parser.add_argument('-o','--output-dir', type=str, required=False, default="./", help='Output directory', dest='outputDir')
  args = parser.parse_args()

  #Check output directory exists
  if not os.path.isdir(args.outputDir) :
    print "ERROR: Output directory does not exist : [%s]" % (args.outputDir)
    sys.exit(-1)


  #Open input file
  rootFile = rh.openFile(args.inputFile)
  if not rootFile : sys.exit(-1)

  numClosestClustersUsed = 3


  #
  # Drift times
  #

  gStyle.SetOptStat(111111)

  canvas = TCanvas("canvas","",800,600)
  h_firstCrossingTime = rh.getFromFile(rootFile,"h_firstCrossingTime")
  h_firstCrossingTime.SetTitle(";Drift time [ns]")
  h_firstCrossingTime.Draw()
  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.16);
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"MTestDriftTimes.eps")


  #
  # Drift times versus DCA
  #

  gStyle.SetOptStat(0)

  canvas = TCanvas("canvas","",800,600)

  #Plot graph
  g_dca_vs_driftTime = rh.getFromFile(rootFile,"g_dca_vs_driftTime")
  #g_dca_vs_driftTime.SetTitle("GARFIELD")
  g_dca_vs_driftTime.GetXaxis().SetTitle("Track DCA to wire [mm]")
  g_dca_vs_driftTime.GetYaxis().SetTitle("Straw drift time [ns]")
  g_dca_vs_driftTime.GetXaxis().SetRangeUser(0.,2.5)
  g_dca_vs_driftTime.GetYaxis().SetRangeUser(0.,100.)
  g_dca_vs_driftTime.SetMarkerStyle(7)
  g_dca_vs_driftTime.Draw("AP")

  #Save canvas
  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"MTestDriftTimeVsDCA.eps")

  #Fit it
  fit = TF1("fit", "[0] + [1]*x", 0.5, 2.5)
  fit.SetParameters(0., 20.) #Initial guesses
  #fit.FixParameter(0,fit.GetParameter(0)) #Fix intercept
  #fit.FixParameter(1,fit.GetParameter(1)) #Fix gradient
  #fit.SetParLimits(1, 0.99, 1.01) #Limit gradient
  g_dca_vs_driftTime.Fit("fit","R") #R enforces range of TF1 for fit
  fitIntercept = fit.GetParameter(0)
  fitSlope = fit.GetParameter(1)
  driftVelocity = 1.e3 / fitSlope
  print ""
  print "+++ Drift velocity =",driftVelocity,"[um/ns]"
  print ""
  #g_dca_vs_driftTime.Draw("AP") #Draw again


  #
  # Track vs cluster DCA
  #

  gStyle.SetOptStat(0)

  canvas = TCanvas("canvas","",800,600)

  legend = TLegend(0.7,0.2,0.9,0.4)

  for i_closest in range(0,numClosestClustersUsed) :

    p_dca_vs_closestClusterDCA = rh.getFromFile(rootFile,"p_dca_vs_closestClusterDCA_%i"%(i_closest))
    p_dca_vs_closestClusterDCA.SetLineColor(i_closest+1)
    p_dca_vs_closestClusterDCA.SetMarkerColor(i_closest+1)
    p_dca_vs_closestClusterDCA.SetTitle(";Track DCA [mm];<Cluster DCA> [mm]")
    p_dca_vs_closestClusterDCA.Draw( "" if i_closest == 0 else "same" )

    legendString = ""
    if i_closest == 0 : legendString = "Closest cluster"
    elif i_closest == 1 : legendString = "Second closest" 
    elif i_closest == 2 : legendString = "Third closest" 
    else :
      print "ERROR: Legend does not support this many layers of cluster closeness"
      sys.exit(-1)
    legend.AddEntry(p_dca_vs_closestClusterDCA, legendString )

  legend.Draw()

  #Save canvas
  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"ClosestClusterDCAVsDCA.eps")


  #
  # Cluster DCA error
  #

  gStyle.SetOptStat(0)

  canvas = TCanvas("canvas","",800,600)

  legend = TLegend(0.7,0.7,0.9,0.9)

  for i_closest in range(0,numClosestClustersUsed) :

    h_closestClusterDCAError = rh.getFromFile(rootFile,"h_closestClusterDCAError_%i"%(i_closest))
    h_closestClusterDCAError.SetLineColor(i_closest+1)
    h_closestClusterDCAError.SetMarkerColor(i_closest+1)
    h_closestClusterDCAError.SetTitle(";Cluster DCA residual to tracker DCA [#mum]")
    h_closestClusterDCAError.Draw( "" if i_closest == 0 else "same" )

    legendString = ""
    if i_closest == 0 : legendString = "Closest cluster"
    elif i_closest == 1 : legendString = "Second closest" 
    elif i_closest == 2 : legendString = "Third closest" 
    else :
      print "ERROR: Legend does not support this many layers of cluster closeness"
      sys.exit(-1)
    legend.AddEntry(h_closestClusterDCAError, legendString )

  legend.Draw()

  #Save canvas
  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"ClosestClusterDCAError.eps")
  
  #TODO Fit "resolution"


  #
  # Resolution
  #

  gStyle.SetOptStat(111111)

  canvas = TCanvas("canvas","",800,600)
  h_recoDCAResiduals = rh.getFromFile(rootFile,"h_recoDCAResiduals")
  h_recoDCAResiduals.SetTitle(";Reconstructed track DCA residual to truth [#mum]")

  f_residuals = TF1("f_recoDCAResiduals", "gaus", -1.5e3, 1.5e3);
  h_recoDCAResiduals.Fit("f_recoDCAResiduals","R")
  fitSigma = f_residuals.GetParameter(2)
  print ""
  print "+++ Gaussian fit to reco DCA residuals : Sigma = %f [um]" % (fitSigma)
  print ""

  h_recoDCAResiduals.Draw()

  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"RecoDCAResiduals.eps")
  
  #TODO Fit "resolution"


  print ""
  print "+++ Done : Output plots in %s" % (args.outputDir)
  print ""

