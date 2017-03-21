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
  parser.add_argument('-pe','--plot-electrons', action='store_true', help='Plot electron drift lines', dest='plotElectronDriftLines')
  parser.add_argument('-pi','--plot-ions', action='store_true', help='Plot ion drift lines', dest='plotIonDriftLines')
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

  #Get num events the event display info was dumped for
  nStoredEventDisplays = t_runInfo.nStoredEventDisplays
  print "Run stored event display info for %i events" % (nStoredEventDisplays)
  print ""

  #
  # Event loop
  #

  #Get event tree
  t_event = rh.getFromFile(rootFile,"Garfield/Events")

  #Get events numbers to process
  eventNums = gh.getEventNumsToProcess(nStoredEventDisplays,args.maxNumEvents,args.firstEvent,args.eventStep)

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


    #
    # Plot raw signal
    #

    numPoints = len(t_event.rawSignalTime)
    g_rawSignal = TGraph(numPoints)
    g_rawSignal.SetTitle( "; Time [ns] ; Current [#muA]" )
  
    for i_pt in range(0,numPoints) :
      g_rawSignal.SetPoint(i_pt,t_event.rawSignalTime[i_pt],t_event.rawSignalCurrent[i_pt])

    g_rawSignal.GetYaxis().SetTitleOffset(1.3)
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
    mg_shapedSignal.SetTitle( ";Time [ns] ; Voltage" )
    #mg_shapedSignal.GetYaxis().SetRangeUser(-300.,100.) #Fixed scale to makes plots easier to compare
    mg_shapedSignal.GetYaxis().SetLabelSize(0.00001)

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
    i_edp_evt = 0   #Counter of electron drift points in whole event
    i_idp_evt = 0   #Counter of ion drift points in whole event

    #Loop over clusters
    for i_clus in range(0,t_event.numClusters) : 

      #Add cluster point (top-down view) to graph
      g_clusterPointsXY.SetPoint(i_clus, t_event.clusterPointX[i_clus], t_event.clusterPointY[i_clus])

      #Note: Latest GARFIELD model only records one drift line per cluster, rather per electron
      #All the secondary electrons tend to be along this path anyway except for rare massive clusters

      #Draw electron drift lines...
      if args.plotElectronDriftLines :

        #Create a plot of the drift line points for this cluster electron
        g_electronDriftLine = TGraph(t_event.electronNumDriftPoints[i_clus])
        g_electronDriftLine.SetMarkerStyle(1)
        g_electronDriftLine.SetMarkerColorAlpha(kBlue,0.999) #Hide
        g_electronDriftLine.SetLineStyle(1)
        g_electronDriftLine.SetLineWidth(1)
        g_electronDriftLine.SetLineColor(kBlue)

        #Loop over drift points for this electron for this cluster
        for i_edp in range(0,t_event.electronNumDriftPoints[i_clus]) : #Loop over drift point for electron

          #Add drift point to plot
          g_electronDriftLine.SetPoint(i_edp, t_event.electronDriftPointX[i_edp_evt], t_event.electronDriftPointY[i_edp_evt])

          i_edp_evt += 1

        #Add to multi-graph
        mg_eventDisplay.Add(g_electronDriftLine)

      #Draw ion drift lines...
      if args.plotIonDriftLines :

        #Create a plot of the drift line points from this cluster ion
        g_ionDriftLine = TGraph(t_event.electronNumDriftPoints[i_clus])
        g_ionDriftLine.SetMarkerStyle(1)
        g_ionDriftLine.SetMarkerColorAlpha(kGreen,0.999) #Hide
        g_ionDriftLine.SetLineStyle(1)
        g_ionDriftLine.SetLineWidth(1)
        g_ionDriftLine.SetLineColor(kGreen)

        #Loop over drift points for this electron for this cluster
        for i_idp in range(0,t_event.ionNumDriftPoints[i_clus]) : #Loop over drift point for electron

          #Add drift point to plot
          g_ionDriftLine.SetPoint(i_idp, t_event.ionDriftPointX[i_idp_evt], t_event.ionDriftPointY[i_idp_evt])

          i_idp_evt += 1

        #Add to multi-graph
        mg_eventDisplay.Add(g_ionDriftLine)

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
    mg_eventDisplay.SetTitle( " ; x [cm] ; y [cm]" )
    mg_eventDisplay.GetXaxis().SetRangeUser(plotXRange[0],plotXRange[1])
    mg_eventDisplay.GetYaxis().SetRangeUser(plotYRange[0],plotYRange[1])
    mg_eventDisplay.GetYaxis().SetTitleOffset(1.4)

    #Add circle representing straw walls (top-down view cross-section)
    strawOutline = TEllipse(0.,0.,.25,.25); #TODO Get radius from data
    strawOutline.SetFillStyle(-1)
    strawOutline.Draw("same")
    
    canvas.Update()

    raw_input("Press Enter to continue...")



