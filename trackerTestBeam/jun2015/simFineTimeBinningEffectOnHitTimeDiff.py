from ROOT import TRandom3, TH1F, TH2F

seed = 12345
rand = TRandom3(seed)

#Book hists
h_driftTimes = TH2F('h_driftTimes','Drift times [ns] ; Layer 0 ; Layer 1',50,0.,50.,50,0.,50.)
h_driftTimeDiffs = TH1F('h_driftTimeDiffs','Drift time diffs [ns]',100,-50.,50.)
h_driftTimeBits = TH2F('h_driftTimeBits','Drift times [fine time bits] ; Layer 0 ; Layer 1',80,0.,80.,80,0.,80.)
h_driftTimeBitDiffs = TH1F('h_driftTimBiteDiffs','Drift time diffs [fine time bits]',160,-80.,80.)

#Generate some events
numEvents = 10000
minDriftTime = 0.
maxDriftTime = 50.
fineTimeBinWidth = 0.625
for i_track in range(0,numEvents) :

  #Generate drift times in doublet (anticorrelated)
  driftTimeFront = rand.Uniform(minDriftTime,maxDriftTime)
  driftTimeBack = maxDriftTime - driftTimeFront

  #Convert drift times into fine time bits (ignoring complication of course time, set all as fine time)
  driftTimeFrontBits = int( driftTimeFront / fineTimeBinWidth )
  driftTimeBackBits = int( driftTimeBack / fineTimeBinWidth )

  #Fill hists
  h_driftTimes.Fill(driftTimeFront,driftTimeBack)
  h_driftTimeDiffs.Fill(driftTimeFront-driftTimeBack)
  h_driftTimeBits.Fill(driftTimeFrontBits,driftTimeBackBits)
  h_driftTimeBitDiffs.Fill(driftTimeFrontBits-driftTimeBackBits)

#Done, plot...
h_driftTimes.Draw("COLZ")
raw_input("Press Enter to continue...")

h_driftTimeDiffs.Draw("COLZ")
raw_input("Press Enter to continue...")

h_driftTimeBits.Draw("COLZ")
raw_input("Press Enter to continue...")

h_driftTimeBitDiffs.Draw("COLZ")
raw_input("Press Enter to continue...")
