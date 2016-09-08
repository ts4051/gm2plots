#

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue
import os, argparse, math, sys
import RootHelper as rh
from collections import OrderedDict

inputRootDir = "/home/scratch/unpacked/"

inputFiles_SCthroughLV = OrderedDict()
inputFiles_SCthroughLV["Read temps"] = inputRootDir + "Lab3UnpackerSummary_00604.root"
inputFiles_SCthroughLV["Don't read temps"] = inputRootDir + "Lab3UnpackerSummary_00603.root"

inputFiles_directSC = OrderedDict()
inputFiles_directSC["Read temps"] = inputRootDir + "Lab3UnpackerSummary_00600.root"
inputFiles_directSC["Don't read temps"] = inputRootDir + "Lab3UnpackerSummary_00602.root"


gStyle.SetOptStat(0)


#
# Define plot function
#

def makePlots(inputFiles,message) :

  #Open all files (keep them in dict so have them in memory simultaneously)
  rootFiles = OrderedDict()
  for key, rootFileName in inputFiles.iteritems() :
    print key,':',rootFileName
    rootFiles[key] = rh.openFile(rootFileName)

  mg_numDigits = TMultiGraph()

  #Loop over files to get each graph to add to mutligraph
  counter = 0
  for key, rootFile in rootFiles.items() :

    counter += 1

    #Get graph
    g_numDigits = rh.getFromFile(rootFile,"straw_unpackers_summary/g_numDigits")

    #Set colors
    g_numDigits.SetMarkerColor(counter)
    g_numDigits.SetLineColor(counter)

    #Add to multigraph to canvas
    mg_numDigits.Add(g_numDigits)


  #
  # Draw the final multigraph
  #

  mg_numDigits.Draw("APL") #Draw once to populate axes
  mg_numDigits.GetXaxis().SetTitle( "Event number" )
  mg_numDigits.GetYaxis().SetTitle( "Num hits" )
  mg_numDigits.GetYaxis().SetTitleOffset(1.2)
  #mg_numDigits.GetXaxis().SetRangeUser(700.,900.)
  mg_numDigits.SetTitle(message)
  mg_numDigits.Draw("APL")
  raw_input("Press Enter to continue...")


#
# Make plots
# 

makePlots(inputFiles_SCthroughLV,"SC through LV controller")
makePlots(inputFiles_directSC,"SC direct to logic board")

