	#Overlay HV scans for Ar:CO2 vs Ar:ethane
#Tom Stuttard

from ROOT import TFile, gROOT, gDirectory, TH1F, TH2F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree, TProfile, kStar
import os, argparse, math, sys
import RootHelper as rh
import garfieldHelper as gh

#
# Main function
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #Get args
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('-e','--ethane-file', type=str, required=False, help='Input ROOT file', dest='ethaneInputFile')
  parser.add_argument('-c','--co2-file', type=str, required=False, help='Input ROOT file', dest='co2InputFile')
  args = parser.parse_args()

  #
  # Combine plots onto single graphs
  #

  mg_gain_vs_wireVoltage = TMultiGraph() 
  mg_hitEfficiency_vs_wireVoltage = TMultiGraph() 

  if args.ethaneInputFile :

    ethaneRootFile = rh.openFile(args.ethaneInputFile)
    g_gain_vs_wireVoltage_ethane = rh.getFromFile(ethaneRootFile,"g_gain_vs_wireVoltage")
    g_hitEfficiency_vs_wireVoltage_ethane = rh.getFromFile(ethaneRootFile,"g_hitEfficiency_vs_wireVoltage")

    g_gain_vs_wireVoltage_ethane.SetMarkerStyle(kStar)
    g_gain_vs_wireVoltage_ethane.SetMarkerColor(kRed)
    g_gain_vs_wireVoltage_ethane.SetLineColorAlpha(kRed,0.99)

    g_hitEfficiency_vs_wireVoltage_ethane.SetMarkerStyle(kStar)
    g_hitEfficiency_vs_wireVoltage_ethane.SetMarkerColor(kRed)
    g_hitEfficiency_vs_wireVoltage_ethane.SetLineColorAlpha(kRed,0.99)

    mg_gain_vs_wireVoltage.Add(g_gain_vs_wireVoltage_ethane)
    mg_hitEfficiency_vs_wireVoltage.Add(g_hitEfficiency_vs_wireVoltage_ethane)

  if args.co2InputFile :

    co2RootFile = rh.openFile(args.co2InputFile)
    g_gain_vs_wireVoltage_co2 = rh.getFromFile(co2RootFile,"g_gain_vs_wireVoltage")
    g_hitEfficiency_vs_wireVoltage_co2 = rh.getFromFile(co2RootFile,"g_hitEfficiency_vs_wireVoltage")

    g_gain_vs_wireVoltage_co2.SetMarkerStyle(kStar)
    g_gain_vs_wireVoltage_co2.SetMarkerColor(kRed)
    g_gain_vs_wireVoltage_co2.SetLineColorAlpha(kRed,0.99)

    g_hitEfficiency_vs_wireVoltage_co2.SetMarkerStyle(kStar)
    g_hitEfficiency_vs_wireVoltage_co2.SetMarkerColor(kRed)
    g_hitEfficiency_vs_wireVoltage_co2.SetLineColorAlpha(kRed,0.99)

    mg_gain_vs_wireVoltage.Add(g_gain_vs_wireVoltage_co2)
    mg_hitEfficiency_vs_wireVoltage.Add(g_hitEfficiency_vs_wireVoltage_co2)


  #
  # Draw
  # 

  mg_gain_vs_wireVoltage.Draw("AP")
  mg_gain_vs_wireVoltage.SetTitle(";Voltage [V];Gain")
  mg_gain_vs_wireVoltage.GetYaxis().SetTitleOffset(1.3)
  mg_gain_vs_wireVoltage.Draw("AP")
  raw_input("Press Enter to continue...")

  mg_hitEfficiency_vs_wireVoltage.Draw("AP")
  mg_hitEfficiency_vs_wireVoltage.SetTitle(";Voltage [V];Efficiency [%]")
  mg_gain_vs_wireVoltage.GetYaxis().SetTitleOffset(1.3)
  mg_hitEfficiency_vs_wireVoltage.Draw("AP")
  raw_input("Press Enter to continue...")


