#Make overall plots of individual GARFIELD runs
#This is currently not well optimised at all, e.g. looping over same stuff multiple times
#Tom Stuttard

from ROOT import TFile, gROOT, TH1F, TH2F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree, TProfile
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
  parser.add_argument('-n','--max-events', type=int, required=False, default=-1, help='Max num events to process', dest='maxNumEvents')
  parser.add_argument('-e','--first-event', type=int, required=False, default=0, help='First event to process', dest='firstEvent')
  parser.add_argument('-s','--event-step', type=int, required=False, default=1, help='Num events to step', dest='eventStep')
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

  h_electronGain = TH1F("h_electronGain",";Gain for primary electron", 100, 1.e4, 5.e7) 
  h_ionGain = TH1F("h_ionGain",";Gain for ion", 100, 1.e5, 5.e7) 
  h_meanGain = TH1F("h_meanGain",";Mean gain", 100, 1.e5, 5.e7) 

  h_numThresholdCrossingsInEvent = TH1F("h_numThresholdCrossingsInEvent",";Num thresholds crossings in event", 6, -0.5, 5.5) 

  #h_firstCrossingTime = TH1F("h_firstCrossingTime",";First threshold crossing time [ns]", 100, 0., 100.) 
  h_firstCrossingTime = TH1F("h_firstCrossingTime",";Drift time [ns]", numTimeBins, timeBinMin, timeBinMax) 

  h_crossingWidth = TH1F("h_crossingWidth",";Time width between first and second threshold crossing [ns]", numTimeBins, timeBinMin, timeBinMax) 

  h_dcaTracks = TH1F("h_dcaTracks","Track Distance of Closest Approach;DCA [mm]", 25, 0., 2.5) 

  h_dcaTriggers = TH1F("h_dcaTriggers","Distance of Closest Approach for tricks causing hits;DCA [mm]", 25, 0., 2.5) 

  p_dca_vs_driftTime = TProfile("p_dca_vs_driftTime",";Track DCA [mm];<Drift time> [ns]", 25, 0., 2.5, timeBinMin, timeBinMax) 

  g_dca_vs_driftTime = TGraph() 

  h_recoDCA = TH1F("h_recoDCA","Reconstructed DCA [mm]", 25, 0., 2.5) 

  h_recoDCAResiduals = TH1F("h_recoDCAResiduals","Reconstructed DCA residual to truth DCA [#mum]", 25, -3.e3, 3.e3) 

  g_dca_vs_recoDCA = TGraph() 

  h_pathLength = TH1F("h_pathLength",";Track path length in gas [mm]", 25, 0., 5.) 

  g_pathLength_vs_numClusters = TGraph() 

  h_numClusters = TH1F("h_numClusters",";Num clusters produced by track", 100,-0.5,99.5) 

  h_clusterDensity = TH1F("h_clusterDensity",";Num clusters produced per unit path length in gas [/cm]", 100,-0.5,99.5) 

  h_numElectronsInCluster = TH1F("h_numElectronsInCluster",";Num primary electrons in a cluster", 30,-0.5,29.5) 

  h_numPrimaryElectrons = TH1F("h_numPrimaryElectrons",";Num primary electrons produced by track", 50, 0.,150.) 

  h_primaryElectronDensity = TH1F("h_primaryElectronDensity",";Num primary electrons produced per unit path length in gas [/cm]", 50, 0.,200.) 

  p_dca_vs_closestClusterDCA = TProfile("p_dca_vs_closestClusterDCA",";Track DCA [mm];<DCA of closest cluster> [mm]", 25, 0., 2.5,0.,2.5) 

  h_closestClusterDCAError = TH1F("h_closestClusterDCAError",";DCA error of closest cluster [#mum]", 15, -0.5e3, 1.e3); 

  p_dca_vs_closestClusterDCAError = TProfile("p_dca_vs_closestClusterDCAError",";Track DCA [mm];<DCA error of closest cluster> [#mum]", 25, 0., 2.5, -0.5e3, 1.e3) 

  g_closestClusterDCA_vs_driftTime = TGraph() 


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
  #raw_input("Press Enter to continue...")

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
      h_firstCrossingTime.Fill( t_event.thresholdCrossingTimes[0] )

    #Crossings width
    if len(t_event.thresholdCrossingTimes) == 2 : 
      crossingWidth = t_event.thresholdCrossingTimes[1] = t_event.thresholdCrossingTimes[0]
      h_crossingWidth.Fill( crossingWidth )

    #Track DCA to wire origin (assumes wire at (0,0,0) and track going in +x (enforced by "checkTrack" above)
    dca = abs( t_event.trackOrigin.y() )
    h_dcaTracks.Fill( dca*10. ) #All tracks
    if len(t_event.thresholdCrossingTimes) > 0 : h_dcaTriggers.Fill( dca*10. ) #Only for events triggering electronics

    #Drift time vs DCA
    #Also process reconstructed DCA from drift time using drift velocity
    if len(t_event.thresholdCrossingTimes) > 0 : #Check there was a threshold crossing
      p_dca_vs_driftTime.Fill( dca*10., t_event.thresholdCrossingTimes[0] )
      g_dca_vs_driftTime.SetPoint( g_dca_vs_driftTime.GetN(), dca*10., t_event.thresholdCrossingTimes[0] )
      recoDCACm = getDCAFroMDriftTime(t_event.thresholdCrossingTimes[0])
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

    #Num primary electrons
    numPrimaryElectrons = 0
    for i_clus in range(0,t_event.numClusters) : 
      numPrimaryElectrons += t_event.numElectronsInCluster[i_clus]
      h_numElectronsInCluster.Fill(t_event.numElectronsInCluster[i_clus])
    h_numPrimaryElectrons.Fill(numPrimaryElectrons)
    primaryElectronDensityPerCm = numPrimaryElectrons/pathLengthInGasCm
    h_primaryElectronDensity.Fill(primaryElectronDensityPerCm)

    #Resolution
    #Intrinsic resolution (e.g. before electronics effects) is based on how close to DCA the closest cluster is produced
    #Additional effects if take multiple clusters to pass threshold
    #First calculate DCA for each cluster (assumes wire origin at 0,0,0 and in z direction), and find min
    if t_event.numClusters > 0 :
      clusterDCAVals = list()
      for i_clus in range(0,t_event.numClusters) : 
        clusterDCA = math.sqrt( math.pow(t_event.clusterPointX[i_clus],2) + math.pow(t_event.clusterPointY[i_clus],2) )
        clusterDCAVals.append(clusterDCA)
      closestClusterDCA = min(clusterDCAVals)
      #Now plot how this compares to the true track DCA
      p_dca_vs_closestClusterDCA.Fill(dca*10.,closestClusterDCA*10.)
      closestClusterDCAError = closestClusterDCA - dca
      h_closestClusterDCAError.Fill(closestClusterDCAError*1.e4)
      p_dca_vs_closestClusterDCAError.Fill(dca*10.,closestClusterDCAError*1.e4)
      if len(t_event.thresholdCrossingTimes) > 0 : #Check there was a threshold crossing
        g_closestClusterDCA_vs_driftTime.SetPoint( g_closestClusterDCA_vs_driftTime.GetN(), closestClusterDCA*10., t_event.thresholdCrossingTimes[0] )

    #Gain
    #Loop over clusters and electrons in cluster
    i_e_evt = 0 #Counter of electrons in clusters in whole event
    for i_clus in range(0,t_event.numClusters) : 
      for i_e in range(0,t_event.numElectronsInCluster[i_clus]) : 
        h_electronGain.Fill(t_event.electronGain[i_e_evt])
        h_ionGain.Fill(t_event.ionGain[i_e_evt])
        h_meanGain.Fill(t_event.meanGain[i_e_evt])
        i_e_evt += 1

  #
  # Draw plots
  # 

  #Gain
  h_electronGain.Draw()
  raw_input("Press Enter to continue...")

#  h_ionGain.Draw()
#  raw_input("Press Enter to continue...")

#  h_meanGain.Draw()
#  raw_input("Press Enter to continue...")

  #Combine DCA histograms on same plot
  h_dcaTracks.SetLineColor(kBlue)
  h_dcaTracks.Draw()
  h_dcaTracks.SetMinimum(0.)
  h_dcaTriggers.SetLineColor(kRed)
  h_dcaTriggers.SetLineStyle(2)
  h_dcaTriggers.Draw("same")
  raw_input("Press Enter to continue...")

  p_dca_vs_closestClusterDCA.Draw()
  raw_input("Press Enter to continue...")

  h_closestClusterDCAError.Draw()
  raw_input("Press Enter to continue...")

  p_dca_vs_closestClusterDCAError.Draw()
  raw_input("Press Enter to continue...")

  #h_numThresholdCrossingsInEvent.Draw()
  #raw_input("Press Enter to continue...")

  h_firstCrossingTime.Draw()
  raw_input("Press Enter to continue...")

  #h_crossingWidth.Draw()
  #raw_input("Press Enter to continue...")

  p_dca_vs_driftTime.Draw()
  raw_input("Press Enter to continue...")

  g_dca_vs_driftTime.SetTitle(";DCA [mm];Drift time [ns]") 
  g_dca_vs_driftTime.SetMarkerStyle(7)
  g_dca_vs_driftTime.Draw("AP") 
  raw_input("Press Enter to continue...")

  g_closestClusterDCA_vs_driftTime.SetTitle(";Closest cluster DCA [mm];Drift time [ns]") 
  g_closestClusterDCA_vs_driftTime.SetMarkerStyle(7)
  g_closestClusterDCA_vs_driftTime.Draw("AP") 
  raw_input("Press Enter to continue...")

  h_recoDCA.Draw()
  raw_input("Press Enter to continue...")

  h_recoDCAResiduals.Draw()
  raw_input("Press Enter to continue...")

  g_dca_vs_recoDCA.SetTitle(";DCA [mm];Reconstructed DCA [mm]") 
  g_dca_vs_recoDCA.SetMarkerStyle(7)
  g_dca_vs_recoDCA.Draw("AP") 
  raw_input("Press Enter to continue...")


#  h_pathLength.Draw()
#  raw_input("Press Enter to continue...")

#  g_pathLength_vs_numClusters.SetTitle(";Track path length in gas [mm];Num clusters")
#  g_pathLength_vs_numClusters.SetMarkerStyle(7)
#  g_pathLength_vs_numClusters.Draw("AP")
#  raw_input("Press Enter to continue...")

#  h_numClusters.Draw()
#  raw_input("Press Enter to continue...")

#  h_clusterDensity.Draw()
#  raw_input("Press Enter to continue...")

#  h_numElectronsInCluster.Draw()
#  raw_input("Press Enter to continue...")

#  h_numPrimaryElectrons.Draw()
#  raw_input("Press Enter to continue...")

#  h_primaryElectronDensity.Draw()
#  raw_input("Press Enter to continue...")

