#Make nicer graph of calo and straw hit positions

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./truthPlots.root", help='Input ROOT file containing plots from StrawAndCaloTruthPlots module', dest='inputFile')
args = parser.parse_args()


#Open input file
rootFile = rh.openFile(args.inputFile)



#
# Function making a nice TGraph
#

def plotHits(particle,station) :

  gr = rh.getFromFile(rootFile,'straw_calo_truth/%s/station_%i/g_hitPosTop' % (particle,station), False )

  gr.Draw("AP")
  gr.GetYaxis().SetTitleOffset(1.5)
  raw_input("Press Enter to continue...")


#
#Plot ahit positons together
#

gStyle.SetOptStat(0)
plotHits("primary_e+",0)

