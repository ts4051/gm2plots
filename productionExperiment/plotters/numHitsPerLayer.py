#TODO

from ROOT import TFile, gROOT, gPad, TCanvas, TPad, gStyle, TGraph, TH1F, TMultiGraph, TAxis, TGaxis, Double, kRed, kGreen, kBlue, kBlack, TEfficiency, TEllipse, TLegend
import os, argparse, math, sys
import RootHelper as rh

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #Get args
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('-p','--pause-for-plots', action='store_true', help='Pause to allow user to look at each plot', dest='pauseForPlots')
  parser.add_argument('-o','--output-dir', type=str, required=False, default="./", help='Output directory for images', dest='outputDir')
  args = parser.parse_args()

  #Check output directory exists
  if not os.path.isdir(args.outputDir) :
    print "ERROR: Output directory does not exist : [%s]" % (args.outputDir)
    sys.exit(-1)

  #Open input files
  simRootFile = rh.openFile("/home/tstuttard/physics/gm2/data/tmp/moduleTestStandSimFullChainPlots.root")
  testBeamRootFile = rh.openFile("/home/tstuttard/physics/gm2/data/tmp/TomPlots.root")
  testStandRootFile = rh.openFile("/home/tstuttard/physics/gm2/data/tmp/Lab3ReadoutPlots.root")

  gStyle.SetOptStat(0)


  #
  # Histograms
  #

  h_sim = rh.getFromFile(simRootFile,"teststand_plots/islands/h_numLayersInIsland")
  h_testBeam = rh.getFromFile(testBeamRootFile,"EventSelection/Islands/h_numGlobalLayersHit")
  h_testStand = rh.getFromFile(testStandRootFile,"StrawEfficiencyUsingScints/DTHR_300mV/h_silverEvents_numLayersHit_signal")

  canvas = TCanvas("c","",800,600)
  h_sim.Scale(1./h_sim.GetEntries())
  h_sim.SetLineColor(1)
  h_sim.SetTitle(";Number of straw layers hit;Fraction")
  h_sim.GetYaxis().SetTitleOffset(1.3)
  h_sim.GetYaxis().SetRangeUser(0.,0.5)
  h_sim.Draw()
  canvas.SetTopMargin(0.05)
  canvas.SetLeftMargin(0.1)
  canvas.SetRightMargin(0.05)
  canvas.SetBottomMargin(0.08)
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"NumLayersEfficiency_sim.eps")
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  canvas = TCanvas("c","",800,600)
  h_testBeam.Scale(1./h_testBeam.GetEntries())
  h_testBeam.SetLineColor(2)
  h_testBeam.SetTitle(";Number of straw layers hit;Fraction")
  h_testBeam.GetYaxis().SetTitleOffset(1.3)
  h_testBeam.GetYaxis().SetRangeUser(0.,0.5)
  h_testBeam.Draw()
  canvas.SetTopMargin(0.05)
  canvas.SetLeftMargin(0.1)
  canvas.SetRightMargin(0.05)
  canvas.SetBottomMargin(0.08)
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"NumLayersEfficiency_testBeam.eps")
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  canvas = TCanvas("c","",800,600)
  h_testStand.Scale(1./h_testStand.GetEntries())
  h_testStand.SetLineColor(3)
  h_testStand.SetTitle(";Number of straw layers hit;Fraction")
  h_testStand.GetYaxis().SetTitleOffset(1.3)
  h_testStand.GetYaxis().SetRangeUser(0.,0.5)
  h_testStand.Draw()
  canvas.SetTopMargin(0.05)
  canvas.SetLeftMargin(0.1)
  canvas.SetRightMargin(0.05)
  canvas.SetBottomMargin(0.08)
  canvas.Draw()
  canvas.SaveAs(args.outputDir+"/"+"NumLayersEfficiency_testStand.eps")
  if args.pauseForPlots : raw_input("Press Enter to continue...")


