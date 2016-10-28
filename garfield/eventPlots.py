#Make plots of individual GARFIELD events
#Tom Stuttard

from ROOT import TFile, gROOT, TCanvas, gStyle, TGraph, TMultiGraph, Double, kRed, kGreen, kBlue, kBlack, TTree, TEllipse
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
  gStyle.SetOptStat(0)


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

  print eventNums

  #Loop over events
  for i_evt in eventNums :

    print "\n\n---------------------------------------------"
    print "Event %i :" % (i_evt)

    #Step tree to current event
    t_event.GetEntry(i_evt)

    #Check the track
    gh.checkTrack(t_event.trackTime, t_event.trackOrigin, t_event.trackDirection)


    #
    # Report basic info
    #

    trackDCA = abs( t_event.trackOrigin.y() )

    print "  Track y = %f [cm]" % (t_event.trackOrigin.y())
    print "  Track DCA = %f [cm]" % (trackDCA)
    print "  Num clusters = %i" % (t_event.numClusters)
    print "  Num threshold crossing = %i" % (len(t_event.thresholdCrossingTimes))
    print ""


    #
    # Plot raw signal
    #

    numPoints = len(t_event.rawSignalTime)
    g_rawSignal = TGraph(numPoints)
    g_rawSignal.SetTitle( "Event %i : Raw signal ; Time [ns] ; Current [#mu A]" % i_evt )
  
    for i_pt in range(0,numPoints) :
      g_rawSignal.SetPoint(i_pt,t_event.rawSignalTime[i_pt],t_event.rawSignalCurrent[i_pt])

    g_rawSignal.Draw("APL")

    raw_input("Press Enter to continue...")


    #
    # Plot shaped signal
    #

    mg_shapedSignal = TMultiGraph()

    #First plot the shaped signal...

    numPoints = len(t_event.shapedSignalTime)
    g_shapedSignal = TGraph(numPoints)
  
    for i_pt in range(0,numPoints) :
      g_shapedSignal.SetPoint(i_pt,t_event.shapedSignalTime[i_pt],t_event.shapedSignalVoltage[i_pt])

    mg_shapedSignal.Add(g_shapedSignal)

    #g_shapedSignal.Draw("APL")

    #Then superimpose with threshold crossing points...

    numPoints = len(t_event.thresholdCrossingTimes)
    if numPoints > 0:

      g_thresholdsCrossings = TGraph(numPoints)
      for i_pt in range(0,numPoints) :
        g_thresholdsCrossings.SetPoint(i_pt,t_event.thresholdCrossingTimes[i_pt],t_event.thresholdCrossingLevels[i_pt])

      g_thresholdsCrossings.SetMarkerStyle(24)
      g_thresholdsCrossings.SetLineColor(2)
      g_thresholdsCrossings.SetMarkerColor(2)

      mg_shapedSignal.Add(g_thresholdsCrossings)

    else:
      print "No threshold crossings, so not adding to plot"

    mg_shapedSignal.Draw("APL") #Must draw before setting properties for TMultiGraph
    mg_shapedSignal.SetTitle( "Event %i : Shaped signal ; Time [ns] ; Voltage [mV]" % i_evt )
    mg_shapedSignal.GetYaxis().SetRangeUser(-300.,100.) #Fixed scale to makes plots easier to compare

    raw_input("Press Enter to continue...")


    #
    # Event display
    #

    #Create a square canvas for the display
    canvas = TCanvas()
    canvas.SetWindowSize(800,800)

    mg_eventDisplay = TMultiGraph()

    #Create top-level graph for drift points (top-down view)
    g_clusterPointsXY = TGraph(t_event.numClusters)
    g_clusterPointsXY.SetMarkerStyle(24)
    g_clusterPointsXY.SetMarkerColor(kBlack)
    g_clusterPointsXY.SetLineColorAlpha(kBlack,0.999) #Hide line

    #Counters used to know what index to use when getting values from trees
    #The trees are flat in each event but have substructure due ti clusters, electrons and drift points
    i_e_evt = 0     #Counter of electrons in clusters in whole event
    i_edp_evt = 0   #Counter of electron drift points in whole event
    i_idp_evt = 0   #Counter of ion drift points in whole event

    #Loop over clusters
    for i_clus in range(0,t_event.numClusters) : 

      #Add cluster point (top-down view) to graph
      g_clusterPointsXY.SetPoint(i_clus, t_event.clusterPointX[i_clus], t_event.clusterPointY[i_clus])

#TODO plot numElectronsInCluster?

      #Loop over electrons in this cluster
      for i_e in range(0,t_event.numElectronsInCluster[i_clus]) : 

        #Draw electron drift lines...

        #Create a plot of the drift line points for this cluster electron
        g_electronDriftLine = TGraph(t_event.electronNumDriftPoints[i_e_evt])
        g_electronDriftLine.SetMarkerStyle(1)
        g_electronDriftLine.SetMarkerColorAlpha(kBlue,0.999) #Hide
        g_electronDriftLine.SetLineStyle(1)
        g_electronDriftLine.SetLineWidth(1)
        g_electronDriftLine.SetLineColor(kBlue)

        #Loop over drift points for this electron for this cluster
        for i_edp in range(0,t_event.electronNumDriftPoints[i_e_evt]) : #Loop over drift point for electron

          #Add drift point to plot
          g_electronDriftLine.SetPoint(i_edp, t_event.electronDriftPointX[i_edp_evt], t_event.electronDriftPointY[i_edp_evt])

          i_edp_evt += 1

        #Draw ion drift lines...

        #Create a plot of the drift line points from this cluster ion
        g_ionDriftLine = TGraph(t_event.electronNumDriftPoints[i_e_evt])
        g_ionDriftLine.SetMarkerStyle(1)
        g_ionDriftLine.SetMarkerColorAlpha(kGreen,0.999) #Hide
        g_ionDriftLine.SetLineStyle(1)
        g_ionDriftLine.SetLineWidth(1)
        g_ionDriftLine.SetLineColor(kGreen)

        #Loop over drift points for this electron for this cluster
        for i_idp in range(0,t_event.ionNumDriftPoints[i_e_evt]) : #Loop over drift point for electron

          #Add drift point to plot
          g_ionDriftLine.SetPoint(i_idp, t_event.ionDriftPointX[i_idp_evt], t_event.ionDriftPointY[i_idp_evt])

          i_idp_evt += 1

        i_e_evt += 1
        
        #Add drift lines to multi-graph
        mg_eventDisplay.Add(g_ionDriftLine)
        mg_eventDisplay.Add(g_electronDriftLine)

    #Add cluster positions to multi-graph
    mg_eventDisplay.Add(g_clusterPointsXY)

    #Draw a line representing particle track
    #Note that this assumes direction is (1,0,0), which presently it is but might need to make more general in future
    plotXRange = [-0.26,0.26] #[cm]
    plotYRange = [-0.26,0.26] #[cm]
    g_track = TGraph(2)
    g_track.SetPoint(0,plotXRange[0],t_event.trackOrigin.y()) #Extreme -ve x point
    g_track.SetPoint(1,plotXRange[1],t_event.trackOrigin.y()) #Extreme +ve x point
    g_track.SetMarkerStyle(1)
    g_track.SetMarkerColorAlpha(kRed,0.999) #Hide
    g_track.SetLineStyle(1)
    g_track.SetLineWidth(1)
    g_track.SetLineColor(kRed)
    mg_eventDisplay.Add(g_track)

    #Draw the whole thing
    mg_eventDisplay.Draw("APL") #Must draw before setting properties for TMultiGraph
    mg_eventDisplay.SetTitle( "Event %i : Track, clusters, and electron and ion drift lines ; x [cm] ; y [cm]" % (i_evt) )
    mg_eventDisplay.GetXaxis().SetRangeUser(plotXRange[0],plotXRange[1])
    mg_eventDisplay.GetYaxis().SetRangeUser(plotYRange[0],plotYRange[1])
    mg_eventDisplay.GetYaxis().SetTitleOffset(1.4)

    #Add circle representing straw walls (top-down view cross-section)
    strawOutline = TEllipse(0.,0.,.25,.25); #TODO Get radius from data
    strawOutline.SetFillStyle(-1)
    strawOutline.Draw("same")
    
    canvas.Update()

    raw_input("Press Enter to continue...")

