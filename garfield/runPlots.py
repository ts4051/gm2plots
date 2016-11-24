#Make overall plots of individual GARFIELD runs
#Tom Stuttard

from ROOT import TFile, gROOT, TH1F, TH2F, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, TTree
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
  #gStyle.SetOptStat(0)

  #
  # Book histos
  #

  h_numThresholdCrossingsInEvent = TH1F("h_numThresholdCrossingsInEvent",";Num thresholds crossings in event", 6, -0.5, 5.5) 

  h_firstCrossingTime = TH1F("h_firstCrossingTime",";First threshold crossing time [ns]", 100, 0., 200.) 

  h_crossingWidth = TH1F("h_crossingWidth",";Time width between first and second threshold crossing [ns]", 100, 0., 200.) 

  h_dcaTracks = TH1F("h_dcaTracks","Track Distance of Closest Approach;DCA [cm]", 25, 0., 0.25) 

  h_dcaTriggers = TH1F("h_dcaTriggers","Distance of Closest Approach for tricks causing hits;DCA [cm]", 25, 0., 0.25) 

  g_dca_vs_driftTime = TGraph() 

  h_pathLength = TH1F("h_pathLength",";Track path length in gas [cm]", 25, 0., 0.5) 

  g_pathLength_vs_numClusters = TGraph() 

  h_numClusters = TH1F("h_numClusters",";Num clusters produced by track", 100,-0.5,99.5) 

  h_clusterDensity = TH1F("h_clusterDensity",";Num clusters produced per unit path length in gas [/cm]", 100,-0.5,99.5) 

  h_numElectronsInCluster = TH1F("h_numElectronsInCluster",";Num primary electrons in a cluster", 30,-0.5,29.5) 

  h_numPrimaryElectrons = TH1F("h_numPrimaryElectrons",";Num primary electrons produced by track", 50, 0.,150.) 

  h_primaryElectronDenisty = TH1F("h_primaryElectronDenisty",";Num primary electrons produced per unit path length in gas [/cm]", 50, 0.,200.) 


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

  #Some params
  strawRadiusCm = 0.25

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
    h_dcaTracks.Fill( dca ) #All tracks
    if len(t_event.thresholdCrossingTimes) > 0 : h_dcaTriggers.Fill( dca ) #Only for events triggering electronic

    #Drift time vs DCA
    if len(t_event.thresholdCrossingTimes) > 0 : #Check there was a threshold crossing
      g_dca_vs_driftTime.SetPoint( g_dca_vs_driftTime.GetN(), dca, t_event.thresholdCrossingTimes[0] )

    #Chord length, chord length vs num clusters, TODO vs signal size
    pathLengthInGasCm = 2. * math.sqrt( math.pow(strawRadiusCm,2) - math.pow(dca,2) )
    h_pathLength.Fill( pathLengthInGasCm )
    g_pathLength_vs_numClusters.SetPoint( g_pathLength_vs_numClusters.GetN(), pathLengthInGasCm, t_event.numClusters )

    #Num clusters
    h_numClusters.Fill(t_event.numClusters)
    clusterDenistyPerCm = t_event.numClusters/pathLengthInGasCm
    h_clusterDensity.Fill(clusterDenistyPerCm)
    #p_dca_vs_clusterDensity.Fill(dca,clusterDenistyPerCm)

    #Num primary electrons
    numPrimaryElectrons = 0
    for i_clus in range(0,t_event.numClusters) : 
      numPrimaryElectrons += t_event.numElectronsInCluster[i_clus]
      h_numElectronsInCluster.Fill(t_event.numElectronsInCluster[i_clus])
    h_numPrimaryElectrons.Fill(numPrimaryElectrons)
    primaryElectronDenistyPerCm = numPrimaryElectrons/pathLengthInGasCm
    h_primaryElectronDenisty.Fill(primaryElectronDenistyPerCm)


  #
  # Draw plots
  # 

  #Combine DCA histograms on same plot
  h_dcaTracks.SetLineColor(kBlue)
  h_dcaTracks.Draw()
  h_dcaTracks.SetMinimum(0.)
  h_dcaTriggers.SetLineColor(kRed)
  h_dcaTriggers.Draw("same")
  raw_input("Press Enter to continue...")

  h_numThresholdCrossingsInEvent.Draw()
  raw_input("Press Enter to continue...")

  h_firstCrossingTime.Draw()
  raw_input("Press Enter to continue...")

  h_crossingWidth.Draw()
  raw_input("Press Enter to continue...")

  g_dca_vs_driftTime.SetTitle(";dca [cm];Drift time [ns]") 
  g_dca_vs_driftTime.SetMarkerStyle(7)
  g_dca_vs_driftTime.Draw("AP") 
  raw_input("Press Enter to continue...")

  h_pathLength.Draw()
  raw_input("Press Enter to continue...")

  g_pathLength_vs_numClusters.SetTitle(";Track path length in gas [cm];Num clusters")
  g_pathLength_vs_numClusters.SetMarkerStyle(7)
  g_pathLength_vs_numClusters.Draw("AP")
  raw_input("Press Enter to continue...")

  h_numClusters.Draw()
  raw_input("Press Enter to continue...")

  h_clusterDensity.Draw()
  raw_input("Press Enter to continue...")

  h_numElectronsInCluster.Draw()
  raw_input("Press Enter to continue...")

  h_numPrimaryElectrons.Draw()
  raw_input("Press Enter to continue...")

  h_primaryElectronDenisty.Draw()
  raw_input("Press Enter to continue...")

