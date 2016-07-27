import numpy as np
import sys, datetime, math, random, argparse
from ROOT import TFile, TCanvas, gStyle, TH1F, TH2F, TGraph2D, TGraph, TMultiGraph, TLegend
#import pylab


#
# Functions
#

#Calculate distance of closest approach of a line to a point
def dca(lineStart,lineEnd,point):

    #d = | ( r0 - r1 ) x ( r0 - r2 ) | / | r2 - r1 |
    #where r0 is point, r1 is line start and r2 is line end
    #http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html

    numerator = np.cross( (point-lineStart), (point-lineEnd) )
    numerator = math.sqrt( np.dot(numerator,numerator) )

    denominator = lineEnd - lineStart
    denominator = math.sqrt( np.dot(denominator,denominator) )

    d = numerator / denominator

    return d


#
# Define params
#

angleRangeDeg = [0,45]
angleStepDeg = 0.5
numAngleSteps = int( ( ( angleRangeDeg[1] - angleRangeDeg[0] ) / angleStepDeg ) + 1 )
strawRadiusMm = 2.5 #TODO update
xRangeMm = [-5,5.]
xStepMm = 0.01
numXSteps = int( ( ( xRangeMm[1] - xRangeMm[0] ) / xStepMm ) + 1 )
wireOffsetBetweenLayersMm = [ 2.5, 0., 2*strawRadiusMm ] #TODO Update
layer0WireOrigin = np.array( [0., 0., 0.] )
layer1WireOrigin = np.array( [ layer0WireOrigin[0] + wireOffsetBetweenLayersMm[0] , layer0WireOrigin[1], layer0WireOrigin[2] + wireOffsetBetweenLayersMm[2] ] )

print "Wire origins = %s, %s" % (str(layer0WireOrigin),str(layer1WireOrigin))


#
# Generate data
#

#Init containers
angleVals = list()
xVals = list()
layer0DCAVals = list()
layer1DCAVals = list()
dcaSumVals = list()

#Loop over angles
for i_angle in range(0,numAngleSteps) :

  angle = angleRangeDeg[0] + ( i_angle * angleStepDeg )

  #Loop over x
  for i_x in range(0,numXSteps) :

    x = xRangeMm[0] + ( i_x * xStepMm )
    #print "x = %f mm" % (x)

    #Get track start and end point (start at z=0 , end at z = 4 * R, x is defined at layer 0 wire z)
    zDepthAtStart = -1. * strawRadiusMm
    trackStart = np.array( [ x + ( zDepthAtStart * math.tan(math.radians(angle)) ) , 0., zDepthAtStart ] )
    zDepthAtEnd = 3. * strawRadiusMm
    trackEnd = np.array( [ x + ( zDepthAtEnd * math.tan(math.radians(angle)) ) , 0., zDepthAtEnd ] )
    #print "Angle = %f deg : x = %f mm : Track start = %s mm : Track end = %s mm" % (angle,x,str(trackStart),str(trackEnd)) 

    #Get DCA in both straws
    layer0DCA = dca(trackStart,trackEnd,layer0WireOrigin)
    layer1DCA = dca(trackStart,trackEnd,layer1WireOrigin)

    #Check hit both straws
    if layer0DCA > strawRadiusMm : continue
    if layer1DCA > strawRadiusMm : continue
  
    #Get DCA sum
    dcaSum = layer0DCA + layer1DCA
    #print "Angle = %f deg : x = %f mm : DCA = %f mm (layer 0), %f mm (layer 1) : DCA sum = %f mm" % (angle,x,layer0DCA,layer1DCA,dcaSum) 

    #Record data for plotting
    angleVals.append(angle)
    xVals.append(x)
    layer0DCAVals.append(layer0DCA)
    layer1DCAVals.append(layer1DCA)
    dcaSumVals.append(dcaSum)


#
# Plot phase space
#

h = TH2F("h_doubletDCASum","DCA sum in doublet [mm]",numXSteps,xRangeMm[0],xRangeMm[1],numAngleSteps,angleRangeDeg[0],angleRangeDeg[1])
for i_point in range(0,len(angleVals)) :
  h.Fill(xVals[i_point],angleVals[i_point],dcaSumVals[i_point])
h.GetXaxis().SetTitle("x [mm]")
h.GetYaxis().SetTitle("Angle of incidence [deg]")
h.Draw("COLZ")
gStyle.SetOptStat(0)
raw_input("Press Enter to continue...")


#
# Plot slices
#

leg = TLegend(0.4,0.6,0.7,0.8)

mg = TMultiGraph()
xSliceGraphs = dict()
xProfilesToPlot = [ 0., 0.5, 1., 1.5, 2.]
for x in xProfilesToPlot : xSliceGraphs[x] = TGraph()
for i_point in range(0,len(xVals)) :
  if xVals[i_point] in xProfilesToPlot : 
    xSliceGraphs[xVals[i_point]].SetPoint(xSliceGraphs[xVals[i_point]].GetN(),angleVals[i_point],dcaSumVals[i_point])
i_plot = 0
for x in xProfilesToPlot : 
  i_color = i_plot+1
  xSliceGraphs[x].SetLineColor(i_color)
  leg.AddEntry(xSliceGraphs[x], "x = %f mm" % (x), "l" )
  mg.Add(xSliceGraphs[x])
  i_plot += 1
mg.Draw("APL") #Draw once to populate axes
mg.GetXaxis().SetTitle( "Angle of incidence [deg]" )
mg.GetYaxis().SetTitle( "Doublet DCA sum [mm]" )
mg.GetYaxis().SetTitleOffset(1.2)
mg.GetYaxis().SetTitleOffset(1.5)
#mg.SetTitle( "Mean electron energy in all xtals per run" )
mg.Draw("APL")

leg.SetFillStyle(0);
leg.SetBorderSize(0);
leg.Draw();

raw_input("Press Enter to continue...")

