#TODO

from ROOT import TFile, gROOT, TCanvas, TPad, gStyle, TGraph, TH1F, TMultiGraph, TAxis, TGaxis, Double, kRed, kGreen, kBlue, kBlack, TEfficiency
import os, argparse, math, sys
import RootHelper as rh

#Get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-i','--input-file', type=str, required=False, default="./truthPlots.root", help='Input ROOT file containing plots from DetectorAcceptancePlots module', dest='inputFile')
parser.add_argument('-p','--pause-for-plots', action='store_true', help='Pause to allow user to look at each plot', dest='pauseForPlots')
parser.add_argument('-o','--output-file', type=str, required=False, default="./acceptancePlotsNew.root", help='Output ROOT file name', dest='outputFile')
args = parser.parse_args()

#Open input file
rootFile = rh.openFile(args.inputFile)


#
# Functions for plotting ratio of two histograms
#

def plotRatioOfTwoHistos(numeratorHist,denominatorHist,title,xtitle,smallestHistScaleFactor=1.) :

  # Get the two histograms
  hn = numeratorHist
  hd = denominatorHist

  # Find which has the largest value
  numeratorHistoHasLargestValue = True if hn.GetMaximum() > hd.GetMaximum() else False

  # Normalise
  #hn.Scale( 1. / hn.Integral() )
  #hd.Scale( 1. / hd.Integral() )

  # Define the Canvas
  c = TCanvas("c", "canvas", 800, 800)

  # Upper plot will be in topPad
  topPad = TPad("topPad", "topPad", 0, 0.3, 1, 1.0)
  topPad.SetBottomMargin(0.04) # Upper and lower plot are joined
  topPad.SetGridx()         # Vertical grid
  topPad.Draw()             # Draw the upper pad: topPad
  topPad.cd()               # topPad becomes the current pad
  hn.SetStats(0)          # No statistics on upper plot

  # Draw histo with largest value first (to get correct y axis range), then overlay other
  if numeratorHistoHasLargestValue : 
    hn.SetTitle(title)
    hn.Draw()               # Draw hn
    hd.Draw("same")         # Draw hd on top of hn
  else :
    hd.SetTitle(title)
    hd.Draw()               # Draw hd
    hn.Draw("same")         # Draw hn on top of hd

  # Draw a scaled version of the smaller histo for ease of viewer
  if smallestHistScaleFactor != 1. :
    hs = hd.Clone("hs") if numeratorHistoHasLargestValue else hn.Clone("hs")
    maxBin = hd.GetMaximumBin() if numeratorHistoHasLargestValue else hn.GetMaximumBin()
    hs.Scale(smallestHistScaleFactor)
    hs.SetStats(0)
    hs.Draw("same")

  # Do not draw the Y axis label on the upper plot and redraw a small
  # axis instead, in order to avoid the first label (0) to be clipped.

  # lower plot will be in pad
  c.cd()          # Go back to the main canvas before defining bottomPad
  bottomPad = TPad("bottomPad", "bottomPad", 0, 0.05, 1, 0.3)
  bottomPad.SetBottomMargin(0.25)
  bottomPad.SetGridx() # vertical grid
  bottomPad.Draw()
  bottomPad.cd()       # bottomPad becomes the current pad

  # Define the ratio plot
  hr = hn.Clone("hr")
  hr.SetLineColor(kBlack)
  #hr.SetMinimum(0.8)  # Define Y ..
  #hr.SetMaximum(1.35) # .. range
  hr.Sumw2()
  hr.SetStats(0)      # No statistics on lower plot
  hr.Divide(hd)
  hr.Scale(100.)      # Ratio -> percentage
  hr.SetMarkerStyle(21)
  hr.Draw("ep")       # Draw the ratio plot

  # hn settings
  hn.SetLineColor(kBlue+1)
  hn.SetLineWidth(2)

  # X axis hn plot settings
  hn.GetXaxis().SetTitleSize(0)
  hn.GetXaxis().SetLabelSize(0)

  # Y axis hn plot settings
  hn.GetYaxis().SetTitleSize(20)
  hn.GetYaxis().SetTitleFont(43)
  hn.GetYaxis().SetTitleOffset(1.55)

  # hd settings
  hd.SetLineColor(kRed)
  hd.SetLineWidth(2)

  # hs settings
  if addScaledPlot :
    if numeratorHistoHasLargestValue : hs.SetLineColor(kRed)
    else : hs.SetLineColor(kBlue+1)
    hs.SetLineWidth(2)
    hs.SetLineStyle(7)

  # Ratio plot (hr) settings
  hr.SetTitle("") # Remove the ratio title
  hr.GetXaxis().SetTitle(xtitle)

  # Y axis ratio plot settings
  hr.GetYaxis().SetTitle("ratio (%)")
  hr.GetYaxis().SetNdivisions(505)
  hr.GetYaxis().SetTitleSize(20)
  hr.GetYaxis().SetTitleFont(43)
  hr.GetYaxis().SetTitleOffset(1.55)
  hr.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  hr.GetYaxis().SetLabelSize(15)

  # X axis ratio plot settings
  hr.GetXaxis().SetTitleSize(20)
  hr.GetXaxis().SetTitleFont(43)
  hr.GetXaxis().SetTitleOffset(4.)
  hr.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  hr.GetXaxis().SetLabelSize(15)

  # Set ratio plot x axis range
  minNonZeroBinContent = 1.e99
  for i_bin in range(1,hr.GetXaxis().GetNbins()+1) :
    binContent = hr.GetBinContent(i_bin)
    if binContent > 0. :
      minNonZeroBinContent = min(binContent,minNonZeroBinContent) 
  hr.GetYaxis().SetRangeUser(minNonZeroBinContent*0.6,hr.GetMaximum()*1.4)

  c.Update()

  # wait so user can see the plot
  if args.pauseForPlots : raw_input("Press Enter to continue...")




def plotEfficiency(e,imgName,title,xtitle,passedScaleFactor=1.) :

  #Get the passed and total histograms
  h_p = e.GetPassedHistogram()
  h_t = e.GetTotalHistogram()

  #Normalise
  h_p_n = h_p.Clone(h_p.GetName()+"_n") #Norm
  h_p_n.Scale(1./float(h_t.GetMaximum()))
  h_t_n = h_t.Clone(h_t.GetName()+"_n") #Norm
  h_t_n.Scale(1./float(h_t.GetMaximum()))

  # Define the Canvas
  c = TCanvas("c", "canvas", 800, 800)

  # Upper plot will be in topPad
  topPad = TPad("topPad", "topPad", 0, 0.3, 1, 1.0)
  topPad.SetBottomMargin(0.04) # Upper and lower plot are joined
  topPad.SetGridx()         # Vertical grid
  topPad.Draw()             # Draw the upper pad: topPad
  topPad.cd()               # topPad becomes the current pad
  h_t_n.SetStats(0)          # No statistics on upper plot

  # Draw total histo first to get correct axis sizes
  h_t_n.SetTitle(title)
  h_t_n.Draw()
  h_p_n.Draw("same")

  # Draw a scaled version of the "passed" histo if required
  if passedScaleFactor != 1. :
    h_p_n_s = h_p_n.Clone(h_p_n.GetName()+"_s")
    h_p_n_s.Scale(passedScaleFactor)
    h_p_n_s.SetStats(0)
    h_p_n_s.Draw("same")

  # Do not draw the Y axis label on the upper plot and redraw a small
  # axis instead, in order to avoid the first label (0) to be clipped.

  # lower plot will be in pad
  c.cd()          # Go back to the main canvas before defining bottomPad
  bottomPad = TPad("bottomPad", "bottomPad", 0, 0.05, 1, 0.3)
  bottomPad.SetBottomMargin(0.25)
  bottomPad.SetGridx() # vertical grid
  bottomPad.Draw()
  bottomPad.cd()       # bottomPad becomes the current pad

  # Define the ratio plot
  h_r = h_p.Clone(h_p.GetName()+"_r")
  h_r.SetTitle("")
  h_r.SetLineColor(kBlack)
  #h_r.SetMinimum(0.8)  # Define Y ..
  #h_r.SetMaximum(1.35) # .. range
  h_r.Sumw2()
  h_r.SetStats(0)      # No statistics on lower plot
  h_r.Divide(h_t)
  h_r.Scale(100.)      # Ratio -> percentage
  h_r.SetMarkerStyle(21)
  h_r.Draw("ep")       # Draw the ratio plot

  # h_t settings
  h_t_n.SetLineColor(kRed)
  h_t_n.SetLineWidth(2)

  # X axis h_t plot settings
  h_t_n.GetXaxis().SetTitleSize(0)
  h_t_n.GetXaxis().SetLabelSize(0)

  # Y axis h_t plot settings
  h_t_n.GetYaxis().SetTitleSize(20)
  h_t_n.GetYaxis().SetTitleFont(43)
  h_t_n.GetYaxis().SetTitleOffset(1.55)

  # h_p settings
  h_p_n.SetLineColor(kBlue)
  h_p_n.SetLineWidth(2)

  # h_p_s settings
  if passedScaleFactor != 1. :
    h_p_n_s.SetLineColor(kBlue)
    h_p_n_s.SetLineWidth(2)
    h_p_n_s.SetLineStyle(7)

  # Ratio plot (h_r) settings
  h_r.SetTitle("") # Remove the ratio title
  h_r.GetXaxis().SetTitle(xtitle)

  # Y axis ratio plot settings
  h_r.GetYaxis().SetTitle("ratio (%)")
  h_r.GetYaxis().SetNdivisions(505)
  h_r.GetYaxis().SetTitleSize(20)
  h_r.GetYaxis().SetTitleFont(43)
  h_r.GetYaxis().SetTitleOffset(1.55)
  h_r.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  h_r.GetYaxis().SetLabelSize(15)

  # X axis ratio plot settings
  h_r.GetXaxis().SetTitleSize(20)
  h_r.GetXaxis().SetTitleFont(43)
  h_r.GetXaxis().SetTitleOffset(4.)
  h_r.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  h_r.GetXaxis().SetLabelSize(15)

  # Set ratio plot y axis range
  minNonZeroBinContent = 1.e99
  for i_bin in range(1,h_r.GetXaxis().GetNbins()+1) :
    binContent = h_r.GetBinContent(i_bin)
    if binContent > 0. :
      minNonZeroBinContent = min(binContent,minNonZeroBinContent) 
  h_r.GetYaxis().SetRangeUser(minNonZeroBinContent*0.8,h_r.GetMaximum()*1.2)

  c.Update()
  c.SaveAs(imgName)

  # wait so user can see the plot
  if args.pauseForPlots : raw_input("Press Enter to continue...")



#
# Plot ratios for all desired histo combinations
#

gStyle.SetOptStat(0)


#
# Beam profile
#

canvas = TCanvas("canvas","",700,600)
h_beamProfile = rh.getFromFile(rootFile,"detector_acceptance/beam/h_vertex_x_vs_y_norm")
#h_beamProfile.Rebin2D(5,5)
h_beamProfile.SetTitle("")
h_beamProfile.GetXaxis().SetTitleOffset(1.1)
h_beamProfile.GetYaxis().SetTitleOffset(1.2)
h_beamProfile.Draw()
canvas.SetTopMargin(0.05);
canvas.SetLeftMargin(0.1);
canvas.SetRightMargin(0.16);
canvas.Draw()
if args.pauseForPlots : raw_input("Press Enter to continue...")


#
# Numbers for acceptance
#

print ""
print "Acceptance info:"
print ""

totalFillsInExperiment = 1.5e8
numMuonsStoredPerFill = 10e3 #After 20 us
totalNumStoredMuonsInExperiment = totalFillsInExperiment * numMuonsStoredPerFill

numCaloStations = 24
numTrackerStations = 3 

def countMuons(histTotal,histECut,numStations) :
  #Get total num
  numMuonsTotal = histTotal.GetEntries()
  numMuonsPerStation = numMuonsTotal / float(numStations)
  #Get num passing E cut
  numMuonsAfterECut = histECut.GetEntries()
  numMuonsAfterECutPerStation = numMuonsAfterECut / float(numStations)
  #Return data
  return numMuonsTotal,numMuonsPerStation,numMuonsAfterECut,numMuonsAfterECutPerStation

#def calcAcceptance() :
#  #Get total num

def percent(N,T) : return 100. * float(N) / float(T) if T > 0 else 0. 

#Get total num muons stored
totalStoredMuons,totalStoredMuonsPerStation, numStoredMuonsAboveECut, numStoredMuonsAboveECutPerStation = \
  countMuons( rh.getFromFile(rootFile,"detector_acceptance/beam/h_vertex_x_vs_y"), rh.getFromFile(rootFile,"detector_acceptance/beam/ECut/h_vertex_x_vs_y"), numCaloStations )

#Get muons accepted by calo
totalCaloMuons,totalCaloMuonsPerStation, numCaloMuonsAboveECut, numCaloMuonsAboveECutPerStation = \
  countMuons( rh.getFromFile(rootFile,"detector_acceptance/calo/h_vertex_x_vs_y"), rh.getFromFile(rootFile,"detector_acceptance/calo/ECut/h_vertex_x_vs_y"), numCaloStations )

#Get muons tracked
totalTrackedMuons,totalTrackedMuonsPerStation, numTrackedMuonsAboveECut, numTrackedMuonsAboveECutPerStation = \
  countMuons( rh.getFromFile(rootFile,"detector_acceptance/tracker/h_vertex_x_vs_y"), rh.getFromFile(rootFile,"detector_acceptance/tracker/ECut/h_vertex_x_vs_y"), numTrackerStations )

percentStoredMuonsAboveECut = percent(numStoredMuonsAboveECut,totalStoredMuons)
print "  Stored muons above E cut = %f%%" \
  % ( percentStoredMuonsAboveECut )

percentCaloMuonsAboveECut = percent(numCaloMuonsAboveECut,numStoredMuonsAboveECut)
print "  Stored muons above E cut that hit calos = %f%% : Per station = %f%%" \
  % ( percentCaloMuonsAboveECut , percent(numCaloMuonsAboveECutPerStation,numStoredMuonsAboveECutPerStation) )

percentTrackedMuons = percent(totalTrackedMuons,totalStoredMuons)
print "  Stored muons that are tracked = %f%% : Per station = %f%%" \
  % ( percentTrackedMuons , percent(totalTrackedMuonsPerStation,totalStoredMuonsPerStation) )

percentTrackedMuonsAboveECut = percent(numTrackedMuonsAboveECut,numStoredMuonsAboveECut)
print "  Stored muons above E cut that are tracked = %f%% : Per station = %f%%" \
  % ( percentTrackedMuonsAboveECut , percent(numTrackedMuonsAboveECutPerStation,numStoredMuonsAboveECutPerStation) )

print ""

numStoredMuonsAboveECutInExperiment = percentStoredMuonsAboveECut * totalNumStoredMuonsInExperiment / 100.
print "  Total num stored muons in experiment = %e" % (totalNumStoredMuonsInExperiment)
print "  Total num stored muons in experiment  above E cut = %e" % (numStoredMuonsAboveECutInExperiment)
print "  Total num calo muons in experiment  above E cut = %e" % ( percentCaloMuonsAboveECut * numStoredMuonsAboveECutInExperiment / 100. )
print "  Total num tracked muons in experiment  above E cut = %e" % ( percentTrackedMuonsAboveECut * numStoredMuonsAboveECutInExperiment / 100. )

print ""


#
# Tracker -> calo beam map
#

#TODO With and without tracker E cut

canvas = TCanvas("canvas","",700,600)

#Get profiles
h_caloProfileECut = rh.getFromFile(rootFile,"detector_acceptance/calo/ECut/h_vertex_x_vs_y")
h_trackerProfileECut = rh.getFromFile(rootFile,"detector_acceptance/tracker/ECut/h_vertex_x_vs_y")

#Normalise to one station
h_caloProfileECut_scaled = h_caloProfileECut.Clone("h_caloProfileECut_scaled")
h_caloProfileECut_scaled.Scale(1./float(numCaloStations))

h_trackerProfileECut_scaled = h_trackerProfileECut.Clone("h_trackerProfileECut_scaled")
h_trackerProfileECut_scaled.Scale(1./float(numTrackerStations))

#Divide calo profile by tracker profile to optain transfer
h_trackerToCaloTransfer = h_caloProfileECut_scaled.Clone("h_trackerToCaloTransfer")
h_trackerToCaloTransfer.Divide(h_trackerProfileECut)

#Now draw it
h_trackerToCaloTransfer.Rebin2D(2,2) #Re-bin to smooth out low stats bins at egdes
h_trackerToCaloTransfer.SetTitle("")
h_trackerToCaloTransfer.GetXaxis().SetTitleOffset(1.1)
h_trackerToCaloTransfer.GetYaxis().SetTitleOffset(1.2)
h_trackerToCaloTransfer.Draw()
canvas.SetTopMargin(0.05);
canvas.SetLeftMargin(0.1);
canvas.SetRightMargin(0.16);
canvas.Draw()
if args.pauseForPlots : raw_input("Press Enter to continue...")



#
# Efficiency 1D plots
#

#No E cut for E
plotEfficiency(rh.getFromFile(rootFile,"detector_acceptance/calo/e_positron_E"),"CaloEEfficiency.eps","","E [GeV]")
plotEfficiency(rh.getFromFile(rootFile,"detector_acceptance/tracker/e_positron_E"),"TrackerEEfficiency.eps","","E [GeV]",8.)

#Use E cut for beam profile
plotEfficiency(rh.getFromFile(rootFile,"detector_acceptance/calo/ECut/e_vertex_x"),"CaloXEfficiency.eps","","x [mm]")
plotEfficiency(rh.getFromFile(rootFile,"detector_acceptance/calo/ECut/e_vertex_y"),"CaloYEfficiency.eps","","y [mm]")
#plotEfficiency(rh.getFromFile(rootFile,"detector_acceptance/calo/ECut/e_vertex_az"),"CaloAzEfficiency.eps","","azimuth [#degree]")

plotEfficiency(rh.getFromFile(rootFile,"detector_acceptance/tracker/ECut/e_vertex_x"),"TrackerXEfficiency.eps","","x [mm]",8.)
plotEfficiency(rh.getFromFile(rootFile,"detector_acceptance/tracker/ECut/e_vertex_y"),"TrackerYEfficiency.eps","","y [mm]",8.)
#plotEfficiency(rh.getFromFile(rootFile,"detector_acceptance/tracker/ECut/e_vertex_az"),"TrackerAzEfficiency.eps","","azimuth [#degree]",8.)


