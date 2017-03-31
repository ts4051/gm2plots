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

  #Get args
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('-i','--input-file', type=str, required=True, help='Input ROOT file', dest='inputFile')
  parser.add_argument('-o','--output-dir', type=str, required=False, default="./", help='Output directory', dest='outputDir')
  parser.add_argument('-v','--high-voltage', type=int, required=False, default=-1, help='High voltage value', dest='highVoltage')
  args = parser.parse_args()

  #Append HV value to file names if one is specified
  highVoltageString = "_%iV" % args.highVoltage if args.highVoltage > -1 else ""

  #Check output directory exists
  if not os.path.isdir(args.outputDir) :
    print "ERROR: Output directory does not exist : [%s]" % (args.outputDir)
    sys.exit(-1)


  #Open input file
  rootFile = rh.openFile(args.inputFile)
  if not rootFile : sys.exit(-1)

  numClosestClustersUsed = 3


  #
  # Efficiency
  #

  gStyle.SetOptStat(0)

  canvas = TCanvas("canvas","",800,600)
  h_dcaTriggers = rh.getFromFile(rootFile,"h_dcaTriggers")
  h_efficiency = h_dcaTriggers.Clone("h_efficiency")
  h_dcaTracks = rh.getFromFile(rootFile,"h_dcaTracks")
  h_efficiency.Divide(h_dcaTracks)
  h_efficiency.Scale(100.)
  h_efficiency.SetTitle(";Track DCA [mm];Efficiency [%]")
  h_efficiency.SetLineStyle(0)
  h_efficiency.SetLineColor(kRed)
  h_efficiency.SetLineWidth(2)
  h_efficiency.GetYaxis().SetTitleOffset(1.3)
  h_efficiency.Draw("hist")
  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.16);
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"GarfieldEfficiency"+highVoltageString+".eps")


  #
  # Drift times
  #

  driftTimeHistName = "h_firstCrossingTime"
  driftTimeHistName += "Smeared"

  gStyle.SetOptStat(0) #111111)

  canvas = TCanvas("canvas","",800,600)
  h_firstCrossingTime = rh.getFromFile(rootFile,driftTimeHistName)
  h_firstCrossingTime.Rebin(2)
  h_firstCrossingTime.Scale( 1./float(h_firstCrossingTime.GetEntries()) )
  h_firstCrossingTime.SetTitle(";Drift time [ns];Normalised counts")
  h_firstCrossingTime.GetYaxis().SetTitleOffset(1.3)
  h_firstCrossingTime.SetLineStyle(0)
  h_firstCrossingTime.SetLineColor(kRed)
  h_firstCrossingTime.SetLineWidth(2)
  h_firstCrossingTime.Draw("hist")
  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.16);
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"GarfieldDriftTimes"+highVoltageString+".eps")


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
  g_dca_vs_driftTime.GetYaxis().SetRangeUser(0.,90.)
  g_dca_vs_driftTime.SetMarkerStyle(7)
  g_dca_vs_driftTime.Draw("AP")

  #Save canvas
  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"GarfieldDriftTimeVsDCA"+highVoltageString+".eps")

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
    p_dca_vs_closestClusterDCA.SetLineWidth(3)
    p_dca_vs_closestClusterDCA.SetMarkerColor(i_closest+1)
    p_dca_vs_closestClusterDCA.SetTitle(";Track DCA to wire [mm];Mean primary ionisation cluster DCA to wire [mm]")
    p_dca_vs_closestClusterDCA.Draw( "hist" if i_closest == 0 else "hist same" )

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
  canvas.SaveAs(args.outputDir+"/"+"GarfieldClosestClusterDCAVsDCA"+highVoltageString+".eps")


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
  canvas.SaveAs(args.outputDir+"/"+"GarfieldClosestClusterDCAError"+highVoltageString+".eps")
 


  #
  # Resolution
  #

  gStyle.SetOptStat(0) #111111)

  canvas = TCanvas("canvas","",800,600)

  h_recoDCAResiduals = rh.getFromFile(rootFile,"h_recoDCAResiduals")
  h_recoDCAResiduals.Scale( 1./float(h_recoDCAResiduals.GetEntries()) )
  h_recoDCAResiduals.SetTitle(";Reconstructed track DCA residual to truth [um];Normalised counts")
  h_recoDCAResiduals.GetYaxis().SetTitleOffset(1.3)
  h_recoDCAResiduals.SetLineStyle(0)
  h_recoDCAResiduals.SetLineColor(kRed)
  h_recoDCAResiduals.SetLineWidth(2)
  #h_recoDCAResiduals.GetXaxis().SetRangeUser(-1500.,1500.)
  h_recoDCAResiduals.Draw("hist")

  canvas.SetTopMargin(0.05);
  canvas.SetLeftMargin(0.1);
  canvas.SetRightMargin(0.05);
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"GarfieldRecoDCAResiduals"+highVoltageString+".eps")

  f_residuals = TF1("f_recoDCAResiduals", "gaus", -1.5e3, 1.5e3);
  h_recoDCAResiduals.Fit("f_recoDCAResiduals","R")
  fitSigma = f_residuals.GetParameter(2)
  print ""
  print "+++ Gaussian fit to reco DCA residuals : Sigma = %0.3g [um] : Histogram RMS = %0.3g" % (fitSigma,h_recoDCAResiduals.GetRMS())
  print ""


  print ""
  print "+++ Done : Output plots in %s" % (args.outputDir)
  print ""

