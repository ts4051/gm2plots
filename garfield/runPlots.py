#Make overall plots of individual GARFIELD runs
#This is currently not well optimised at all, e.g. looping over same stuff multiple times
#Tom Stuttard

#Some notes:
#
#  "Clusters" in GARFIELD refer to a primary ionisation electron and the subsequent secondary electrons it produces, 
#  excluding the avalanche (which is handled separately)
#
#  "Gain" is the total number of electrons produced for a primary ionisation, including the avalanche
#

from ROOT import TFile, gROOT, TH1F, TH2F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree, TProfile
import os, argparse, math, sys, random
import RootHelper as rh
import garfieldHelper as gh
from array import *

#Logarithmic bins (https://root.cern.ch/root/roottalk/roottalk06/1213.html)
def BinLogX(h) :
  axis = h.GetXaxis()
  bins = axis.GetNbins()
  xMin = axis.GetXmin()
  xMax = axis.GetXmax()
  width = (xMax - xMin) / bins
  new_bins = list()
  for i in range(0,bins+1) : new_bins.append( pow(10, xMin + (i * width) ) )
  bins_array = array('d',new_bins)
  axis.Set(bins, bins_array)



#
# Main function
#

if __name__ == "__main__" : #Only run if this script is the one execued (not imported)

  #Get args
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('-i','--input-file', type=str, required=True, help='Input ROOT file', dest='inputFile')
  parser.add_argument('-n','--max-events', type=int, required=False, default=-1, help='Max num events to process', dest='maxNumEvents')
  parser.add_argument('-e','--first-event', type=int, required=False, default=0, help='First event to process', dest='firstEvent')
  parser.add_argument('-s','--event-step', type=int, required=False, default=1, help='Num events to step', dest='eventStep')
  parser.add_argument('-p','--pause-for-plots', action='store_true', help='Pause to allow user to look at each plot', dest='pauseForPlots')
  args = parser.parse_args()

  #Open input file
  rootFile = rh.openFile(args.inputFile)
  if not rootFile : sys.exit(-1)

  #Init plotting
  gStyle.SetOptStat(111111)

  #Derift velocity
  driftVelocityUmPerNs = 48.3 #From test beam
  def getDCAFroMDriftTime(driftTimeNs) : return driftVelocityUmPerNs * 1.e-4 * driftTimeNs


  #
  # Book histos
  #

  #Determine time binning
  timeBinWidthNs = 2.5 #Fine time issue
  numTimeBins = 100
  binRangeNs = float(numTimeBins) * timeBinWidthNs
  timeCentralBinNs = 0.
  timeBinMin = timeCentralBinNs - ( binRangeNs / 2. )
  timeBinMax = timeCentralBinNs + ( binRangeNs / 2. )

  t0Resolution = 2.2 #[ns] for cosmics test stand, https://muon.npl.washington.edu/elog/g2/Straw+detectors/134

  h_electronGain = TH1F("h_electronGain",";Gain for electron (primary or secondary)", 100, 1.e4, 5.e7) 

  h_clusterGain = TH1F("h_clusterGain",";Total gain for all electrons in cluster", 100, 1.e4, 5.e7) 

  h_numThresholdCrossingsInEvent = TH1F("h_numThresholdCrossingsInEvent",";Num thresholds crossings in event", 6, -0.5, 5.5) 

  #h_firstCrossingTime = TH1F("h_firstCrossingTime",";First threshold crossing time [ns]", 100, 0., 100.) 
  h_firstCrossingTime = TH1F("h_firstCrossingTime",";Drift time [ns]", numTimeBins, timeBinMin, timeBinMax) 
  h_firstCrossingTimeSmeared = TH1F("h_firstCrossingTimeSmeared","t0 resolution = %0.3g [ns];Drift time [ns]"%t0Resolution, numTimeBins, timeBinMin, timeBinMax) 

  h_crossingWidth = TH1F("h_crossingWidth",";Time width between first and second threshold crossing [ns]", numTimeBins, timeBinMin, timeBinMax) 

  h_dcaTracks = TH1F("h_dcaTracks","Track Distance of Closest Approach;DCA [mm]", 25, 0., 2.5) 

  h_dcaTriggers = TH1F("h_dcaTriggers","Distance of Closest Approach for tricks causing hits;DCA [mm]", 25, 0., 2.5) 

  p_dca_vs_driftTime = TProfile("p_dca_vs_driftTime",";Track DCA [mm];<Drift time> [ns]", 25, 0., 2.5, timeBinMin, timeBinMax) 

  g_dca_vs_driftTime = TGraph() 

  h_recoDCA = TH1F("h_recoDCA","Reconstructed DCA [mm]", 25, 0., 2.5) 

  h_recoDCAResiduals = TH1F("h_recoDCAResiduals","Reconstructed DCA residual to truth DCA [#mum]", 50, -3.e3, 3.e3) 

  g_dca_vs_recoDCA = TGraph() 

  h_pathLength = TH1F("h_pathLength",";Track path length in gas [mm]", 25, 0., 5.) 

  g_pathLength_vs_numClusters = TGraph() 

  h_numClusters = TH1F("h_numClusters",";Num clusters produced by track", 100,-0.5,99.5) 

  h_clusterDensity = TH1F("h_clusterDensity",";Num clusters produced per unit path length in gas [/cm]", 100,-0.5,99.5) 

  h_numElectronsInCluster_zoom = TH1F("h_numElectronsInCluster_zoom",";Num electrons liberated in a cluster", 30,-0.5,29.5) 
  h_numElectronsInCluster = TH1F("h_numElectronsInCluster",";Num electrons liberated in a cluster", int(1e4),0,1.e4) 
  #BinLogX(h_numElectronsInCluster)

  h_numElectrons = TH1F("h_numElectrons",";Total num electrons liberated by track", 50, 0.,150.) 

  numClosestClustersToUse = 3
  p_dca_vs_closestClusterDCA = list()
  h_closestClusterDCAError = list()
  p_dca_vs_closestClusterDCAError = list()
  g_closestClusterDCA_vs_driftTime = list()
  for i_closest in range(0,numClosestClustersToUse) :
    p_dca_vs_closestClusterDCA.append( TProfile("p_dca_vs_closestClusterDCA_%i"%(i_closest),";Track DCA [mm];<DCA of %i'th closest cluster> [mm]"%(i_closest), 25, 0., 2.5,0.,2.5) )
    h_closestClusterDCAError.append( TH1F("h_closestClusterDCAError_%i"%(i_closest),";DCA error of %i'th closest cluster [#mum]"%(i_closest), 22, -0.1e3, 1.e3) )
    p_dca_vs_closestClusterDCAError.append( TProfile("p_dca_vs_closestClusterDCAError_%i"%(i_closest),";Track DCA [mm];<DCA error of %i'th closest cluster> [#mum]"%(i_closest), 25, 0., 2.5, -0.5e3, 1.e3) )
    g_closestClusterDCA_vs_driftTime.append( TGraph() )


  #
  # Run info
  #

  #Get run info tree
  t_runInfo = rh.getFromFile(rootFile,"Garfield/RunInfo")
  t_runInfo.GetEntry(0) #Only one entry

  #Dump some print
  gh.dumpRunInfo(t_runInfo)


  #
  # Event loop
  #

  #Get event tree
  t_event = rh.getFromFile(rootFile,"Garfield/Events")

  #Get events numbers to process
  eventNums = gh.getEventNumsToProcess(t_event.GetEntries(),args.maxNumEvents,args.firstEvent,args.eventStep)

  #Plot raw signal for this event #TODO REMOVE
  #t_event.Draw("rawSignalCurrent:rawSignalTime")
  #if args.pauseForPlots : raw_input("Press Enter to continue...")

  #Loop over events
  for i_evt in eventNums :

    if i_evt % 100 == 0 : print "Event %i" % (i_evt) #TODO % done instead

    #Step tree to current event
    t_event.GetEntry(i_evt)

    #Check the track
    gh.checkTrack(t_event.trackTime, t_event.trackOrigin, t_event.trackDirection)


    #
    # Fill plots
    #

    #Num times the ASDQ threshold was crossed 
    h_numThresholdCrossingsInEvent.Fill( len(t_event.thresholdCrossingTimes) )

    #TODO Investigate cases with single threshold crossing

    #Threshold crossing time (first edge only)
    if len(t_event.thresholdCrossingTimes) > 0 : #Check there was a threshold crossing
      driftTime = min(t_event.thresholdCrossingTimes) #Drift time is the first crossing
      h_firstCrossingTime.Fill(driftTime)
      smearedDriftTime = random.gauss(driftTime,t0Resolution) #Try smearing drift time
      h_firstCrossingTimeSmeared.Fill(smearedDriftTime)

    #Crossings width
    if len(t_event.thresholdCrossingTimes) == 2 : 
      crossingWidth = max(t_event.thresholdCrossingTimes) - min(t_event.thresholdCrossingTimes)
      h_crossingWidth.Fill( crossingWidth )

    #Track DCA to wire origin (assumes wire at (0,0,0) and track going in +x (enforced by "checkTrack" above)
    dca = abs( t_event.trackOrigin.y() )
    h_dcaTracks.Fill( dca*10. ) #All tracks
    if len(t_event.thresholdCrossingTimes) > 0 : h_dcaTriggers.Fill( dca*10. ) #Only for events triggering electronics

    #Drift time vs DCA
    #Also process reconstructed DCA from drift time using drift velocity
    if len(t_event.thresholdCrossingTimes) > 0 : #Check there was a threshold crossing
      p_dca_vs_driftTime.Fill( dca*10., driftTime )
      g_dca_vs_driftTime.SetPoint( g_dca_vs_driftTime.GetN(), dca*10., driftTime )
      recoDCACm = getDCAFroMDriftTime(driftTime)
      recoDCAResidualCm = recoDCACm - dca
      h_recoDCA.Fill( recoDCACm*10. )
      h_recoDCAResiduals.Fill( recoDCAResidualCm*1.e4 )
      g_dca_vs_recoDCA.SetPoint( g_dca_vs_recoDCA.GetN(), dca*10., recoDCACm*10. )

    #Chord length, chord length vs num clusters, TODO vs signal size
    pathLengthInGasCm = 2. * math.sqrt( math.pow(t_runInfo.strawRadiusMm*1.e-1,2) - math.pow(dca,2) )
    h_pathLength.Fill( pathLengthInGasCm*10. )
    g_pathLength_vs_numClusters.SetPoint( g_pathLength_vs_numClusters.GetN(), pathLengthInGasCm*10., t_event.numClusters )

    #Num clusters
    h_numClusters.Fill(t_event.numClusters)
    clusterDensityPerCm = t_event.numClusters/pathLengthInGasCm
    h_clusterDensity.Fill(clusterDensityPerCm)
    #p_dca_vs_clusterDensity.Fill(dca,clusterDensityPerCm)

    #Num liberated electrons
    numElectrons = 0
    for i_clus in range(0,t_event.numClusters) : 
      numElectrons += t_event.numElectronsInCluster[i_clus]
      h_numElectronsInCluster_zoom.Fill(t_event.numElectronsInCluster[i_clus])
      h_numElectronsInCluster.Fill(t_event.numElectronsInCluster[i_clus])
    h_numElectrons.Fill(numElectrons)

    #Resolution
    #Intrinsic resolution (e.g. before electronics effects) is based on how close to DCA the closest cluster is produced
    #Additional effects if take multiple clusters to pass threshold
    #First calculate DCA for each cluster (assumes wire origin at 0,0,0 and in z direction), and find min
    if t_event.numClusters > 0 :
      clusterDCAVals = list()
      for i_clus in range(0,t_event.numClusters) : 
        clusterDCA = math.sqrt( math.pow(t_event.clusterPointX[i_clus],2) + math.pow(t_event.clusterPointY[i_clus],2) )
        clusterDCAVals.append(clusterDCA)
      clusterDCAVals.sort() #Ascending order
      for i_closest in range(0,min(numClosestClustersToUse,t_event.numClusters)) :
        closestClusterDCA = clusterDCAVals[i_closest]
        #Now plot how this compares to the true track DCA
        p_dca_vs_closestClusterDCA[i_closest].Fill(dca*10.,closestClusterDCA*10.)
        closestClusterDCAError = closestClusterDCA - dca
        h_closestClusterDCAError[i_closest].Fill(closestClusterDCAError*1.e4)
        p_dca_vs_closestClusterDCAError[i_closest].Fill(dca*10.,closestClusterDCAError*1.e4)
        if len(t_event.thresholdCrossingTimes) > 0 : #Check there was a threshold crossing
          g_closestClusterDCA_vs_driftTime[i_closest].SetPoint( g_closestClusterDCA_vs_driftTime[i_closest].GetN(), closestClusterDCA*10., driftTime )

    #Gain
    #Loop over clusters and electrons in cluster
    i_e_evt = 0 #Counter of electrons in clusters in whole event
    for i_clus in range(0,t_event.numClusters) : 
      h_clusterGain.Fill(t_event.clusterGain[i_clus])
      for i_e in range(0,t_event.numElectronsInCluster[i_clus]) : 
        h_electronGain.Fill(t_event.electronGain[i_e_evt])
        i_e_evt += 1

  print "Done processing files"


  #
  # Draw plots
  # 

  #Gain
  h_electronGain.Draw()
  if args.pauseForPlots : raw_input("Press Enter to continue...")

#  h_ionGain.Draw()
#  if args.pauseForPlots : raw_input("Press Enter to continue...")

#  h_meanGain.Draw()
#  if args.pauseForPlots : raw_input("Press Enter to continue...")

  #Combine DCA histograms on same plot
  h_dcaTracks.SetLineColor(kBlue)
  h_dcaTracks.Draw()
  h_dcaTracks.SetMinimum(0.)
  h_dcaTriggers.SetLineColor(kRed)
  h_dcaTriggers.SetLineStyle(2)
  h_dcaTriggers.Draw("same")
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  #h_numThresholdCrossingsInEvent.Draw()
  #if args.pauseForPlots : raw_input("Press Enter to continue...")

  h_firstCrossingTime.Draw()
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  h_firstCrossingTimeSmeared.Draw()
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  #h_crossingWidth.Draw()
  #if args.pauseForPlots : raw_input("Press Enter to continue...")

  p_dca_vs_driftTime.Draw()
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  g_dca_vs_driftTime.SetTitle(";DCA [mm];Drift time [ns]") 
  g_dca_vs_driftTime.SetMarkerStyle(7)
  g_dca_vs_driftTime.Draw("AP") 
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  h_recoDCA.Draw()
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  h_recoDCAResiduals.Draw()
  if args.pauseForPlots : raw_input("Press Enter to continue...")

  g_dca_vs_recoDCA.SetTitle(";DCA [mm];Reconstructed DCA [mm]") 
  g_dca_vs_recoDCA.SetMarkerStyle(7)
  g_dca_vs_recoDCA.Draw("AP") 
  if args.pauseForPlots : raw_input("Press Enter to continue...")


#  h_pathLength.Draw()
#  if args.pauseForPlots : raw_input("Press Enter to continue...")

#  g_pathLength_vs_numClusters.SetTitle(";Track path length in gas [mm];Num clusters")
#  g_pathLength_vs_numClusters.SetMarkerStyle(7)
#  g_pathLength_vs_numClusters.Draw("AP")
#  if args.pauseForPlots : raw_input("Press Enter to continue...")

#  h_numClusters.Draw()
#  if args.pauseForPlots : raw_input("Press Enter to continue...")

#  h_clusterDensity.Draw()
#  if args.pauseForPlots : raw_input("Press Enter to continue...")

#  h_numElectronsInCluster.Draw()
#  if args.pauseForPlots : raw_input("Press Enter to continue...")

#  h_numElectrons.Draw()
#  if args.pauseForPlots : raw_input("Press Enter to continue...")

#  h_clusterDensity.Draw()
#  if args.pauseForPlots : raw_input("Press Enter to continue...")


  #
  # Write to file
  #

  outputFileName = "runPlots.root"
  outputFile = TFile(outputFileName,"RECREATE")

  h_electronGain.Write()
  h_clusterGain.Write()
  h_dcaTracks.Write()
  h_dcaTriggers.Write()
  h_numThresholdCrossingsInEvent.Write()
  h_firstCrossingTime.Write()
  h_firstCrossingTimeSmeared.Write()
  p_dca_vs_driftTime.Write()
  g_dca_vs_driftTime.SetName("g_dca_vs_driftTime") 
  g_dca_vs_driftTime.Write() 
  h_recoDCA.Write()
  h_recoDCAResiduals.Write()
  g_dca_vs_recoDCA.SetName("g_dca_vs_recoDCA") 
  g_dca_vs_recoDCA.Write() 
  h_pathLength.Write()
  g_pathLength_vs_numClusters.SetName("g_pathLength_vs_numClusters")
  g_pathLength_vs_numClusters.Write()
  h_numClusters.Write()
  h_clusterDensity.Write
  h_numElectronsInCluster.Write()
  h_numElectronsInCluster_zoom.Write()
  h_numElectrons.Write()
  h_clusterDensity.Write()

  for i_closest in range(0,numClosestClustersToUse) :
    p_dca_vs_closestClusterDCA[i_closest].Write()
    h_closestClusterDCAError[i_closest].Write()
    p_dca_vs_closestClusterDCAError[i_closest].Write()
    g_closestClusterDCA_vs_driftTime[i_closest].SetTitle(";Closest cluster DCA [mm];Drift time [ns]") 
    g_closestClusterDCA_vs_driftTime[i_closest].SetName("g_closestClusterDCA_vs_driftTime_%i" % (i_closest)) 
    g_closestClusterDCA_vs_driftTime[i_closest].Write() 

  outputFile.Close()

  print "+++ Done : Output file = %s" % (outputFileName)

