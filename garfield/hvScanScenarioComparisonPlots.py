#Overlay scans for differnt particles, gases, DTHR, B fields, whatever...
#Tom Stuttard

from ROOT import TFile, gROOT, gDirectory, TH1F, TH2F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree, TProfile, kStar, TCanvas, TLegend
import os, argparse, math, sys, collections
import RootHelper as rh
import garfieldHelper as gh

#
# Main function
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #Get args
  parser = argparse.ArgumentParser(description='')
  args = parser.parse_args()

  inputFiles = collections.OrderedDict()
  topDir = "/Users/stuttard/physics/gm2/software/offline/gm2plots/garfield"
  inputFiles["Cosmic-ray test-stand"] = os.path.join(topDir,"hvScanPlots_cosmics.root")
  inputFiles["MTest 120 GeV protons"] = os.path.join(topDir,"hvScanPlots_mtest.root")
  inputFiles["Sr90 test-stand"] = os.path.join(topDir,"hvScanPlots_sr90.root")
  inputFiles["g-2 experiment"] = os.path.join(topDir,"hvScanPlots_default.root")

  #
  # Combine plots onto single graphs
  #

  mg_gain_vs_wireVoltage = TMultiGraph() 
  l_gain_vs_wireVoltage = TLegend(0.2,0.6,0.5,0.8)

  mg_hitEfficiency_vs_wireVoltage = TMultiGraph() 
  l_hitEfficiency_vs_wireVoltage = TLegend(0.5,0.2,0.9,0.4)


  i = 1
  for key,f in inputFiles.items() :

    rootFile = rh.openFile(f)
    g_gain_vs_wireVoltage = rh.getFromFile(rootFile,"g_gain_vs_wireVoltage")
    g_hitEfficiency_vs_wireVoltage = rh.getFromFile(rootFile,"g_hitEfficiency_vs_wireVoltage")

    g_gain_vs_wireVoltage.SetMarkerStyle(8)
    g_gain_vs_wireVoltage.SetMarkerSize(1)
    g_gain_vs_wireVoltage.SetMarkerColor(i)
    g_gain_vs_wireVoltage.SetLineColor(i)
    g_gain_vs_wireVoltage.SetLineWidth(3)
    g_gain_vs_wireVoltage.SetLineStyle(1)

    g_hitEfficiency_vs_wireVoltage.SetMarkerStyle(1)
    g_hitEfficiency_vs_wireVoltage.SetMarkerColor(i)
    g_hitEfficiency_vs_wireVoltage.SetLineColor(i)
    g_hitEfficiency_vs_wireVoltage.SetLineWidth(3)

    l_gain_vs_wireVoltage.AddEntry(g_gain_vs_wireVoltage, key, "l" )
    l_hitEfficiency_vs_wireVoltage.AddEntry(g_hitEfficiency_vs_wireVoltage, key, "l" )

    mg_gain_vs_wireVoltage.Add(g_gain_vs_wireVoltage)
    mg_hitEfficiency_vs_wireVoltage.Add(g_hitEfficiency_vs_wireVoltage)

    i += 1


  #
  # Draw
  # 

  c1 = TCanvas("c1","",900,600)
  c1.SetLogy()
  mg_gain_vs_wireVoltage.Draw("AP")
  mg_gain_vs_wireVoltage.SetTitle(";Wire voltage [V];Electron multiplication gain")
  mg_gain_vs_wireVoltage.GetYaxis().SetTitleOffset(1.3)
  mg_gain_vs_wireVoltage.Draw("APL")
  l_gain_vs_wireVoltage.SetFillStyle(0)
  l_gain_vs_wireVoltage.SetBorderSize(0)
  l_gain_vs_wireVoltage.Draw()
  c1.Draw()
  c1.SaveAs("GainVsHV.eps")
  raw_input("Press Enter to continue...")

  c2 = TCanvas("c2","",900,600)
  mg_hitEfficiency_vs_wireVoltage.Draw("AP")
  mg_hitEfficiency_vs_wireVoltage.SetTitle(";Wire voltage [V];Hit rate [arb. units]")
#  mg_hitEfficiency_vs_wireVoltage.SetTitle(";Wire voltage [V];Straw efficiency [%]")
  mg_gain_vs_wireVoltage.GetYaxis().SetTitleOffset(1.3)
  mg_gain_vs_wireVoltage.GetYaxis().SetLabelSize(0.)
  mg_hitEfficiency_vs_wireVoltage.Draw("APL")
  l_hitEfficiency_vs_wireVoltage.SetFillStyle(0)
  l_hitEfficiency_vs_wireVoltage.SetBorderSize(0)
  l_hitEfficiency_vs_wireVoltage.Draw()
  c2.Draw()
#  c2.SaveAs("EfficiencyVsHV.eps")
  c2.SaveAs("SimHitRateVsHV.eps")
  raw_input("Press Enter to continue...")


