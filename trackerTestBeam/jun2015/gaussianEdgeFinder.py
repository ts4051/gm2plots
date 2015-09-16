#Prototyping some edge finding algorithms for finding rising edge of drift spectrum

from ROOT import TRandom3, TH1F
from collections import OrderedDict, deque
import operator

seed = 12345
rand = TRandom3(seed)

#
# Generate plot to analyse
#

#Generate a Gaussian
h_gaussian = TH1F('h_gaussian','',100,-50.,50.)
numPoints = 10000
for i_pt in range(0,numPoints) :
  x = rand.Gaus(0.,5.)
  h_gaussian.Fill(x)

#Add noise
numNoise = int(numPoints/10)
for i_noise in range(0,numNoise) :
  x = rand.Uniform(-50.,50.)
  h_gaussian.Fill(x)

#Done, plot
h_gaussian.Draw()
raw_input("Press Enter to continue...")

#
# Find edge
#

#Get bin content
numBins = h_gaussian.GetXaxis().GetNbins()
bins = OrderedDict()
for i_bin in range(1,numBins+1) : #Bin 0 is underflow, bin nbins+1 is overflow
  bins[h_gaussian.GetBinCenter(i_bin)] = h_gaussian.GetBinContent(i_bin) 
#print bins

#Get hist bin content range
minBinContent = min(bins.values())
maxBinContent =  max(bins.values())
binContentRange = maxBinContent - minBinContent
#print 'Bin content range = %f' % (binContentRange)

#Option 1 : Sharpest region of rise
recentGradients = deque(maxlen=3) #Last few gradients
recentGradientSums = OrderedDict() #Sum of last few gradients for each bin
for i_bin in range(1,len(bins)) : #Start at second bin as need to compare to i-1
  binGradient = bins.values()[i_bin] - bins.values()[i_bin-1] #Ignoring "/ deltaX", as same for every bin
  #print 'Gradient : %i : %f : %f' % (i_bin,bins.keys()[i_bin],binGradient)
  recentGradients.append(binGradient)
  recentGradientSums[bins.keys()[i_bin]] = sum(recentGradients)
binCentersWithMaxLocalGradients = [k for k,v in recentGradientSums.items() if v==max(recentGradientSums.values())]
print 'Bin center(s) with highest rising gradient =',binCentersWithMaxLocalGradients

#Option 2 : First region of consistent rise
recentGradients = deque(maxlen=3) #Last few gradients
for i_bin in range(1,len(bins)) : #Start at second bin as need to compare to i-1
  binGradient = bins.values()[i_bin] - bins.values()[i_bin-1] #Ignoring "/ deltaX", as same for every bin
  recentGradients.append(binGradient)
  if all( gradient > 0. for gradient in recentGradients) : #If all recent gradients are positive
    print 'Bin center at start of rise =',bins.keys()[i_bin-(len(recentGradients)-1)]
    break

