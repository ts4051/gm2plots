from ROOT import TRandom3, TH2F

seed = 12345
rand = TRandom3(seed)

driftTimeMin = 0.
driftTimeMax = 50.

h_numDigitsVsWidth = TH2F('h_numDigitsVsWidth',';Num digits in island;Island time width [ns]',10,-0.5,9.5,50,0.,70.)

#Generate some islands
numIslands = 100000
for i_island in range(0,numIslands) :

  #Generate some random drift times (not anticorrelated)
  numDigits = int(rand.Uniform(2.,10.))
  driftTimes = list()
  for i_digit in range(0,numDigits) :
    driftTimes.append( rand.Uniform(driftTimeMin,driftTimeMax) )

  #Get island time width
  width = max(driftTimes)-min(driftTimes) if len(driftTimes)>0 else 0.
  h_numDigitsVsWidth.Fill(numDigits,width)

#Done, plot
h_numDigitsVsWidth.Draw('COLZ')
raw_input("Press Enter to continue...")

