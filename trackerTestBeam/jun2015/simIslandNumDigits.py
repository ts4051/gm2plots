from ROOT import TRandom3, TH1F

seed = 12345
rand = TRandom3(seed)

efficiency = 0.6

h_numHits = TH1F('h_numHits','Num hits (out of max 4)',5,-0.5,4.5)

#Generate some tracks
numTracks = 10000
totalHits = 0
totalRecoEvents = 0
for i_track in range(0,numTracks) :

  #Determine whether each straw is hit
  numHits = 0
  for i_straw in range(0,4) :
    if rand.Uniform(0.,1.) < efficiency : numHits += 1

  #Fill hist
  h_numHits.Fill(numHits)

  totalHits += numHits
  if numHits == 4 : totalRecoEvents += 1

calculatedEfficiency = float(totalHits) / float(numTracks*4)
recoCandidateEfficiency = float(totalRecoEvents) / float(numTracks)
print 'User efficiency =',efficiency,': Generated efficiency =',calculatedEfficiency,': Reco candidate efficiency =',recoCandidateEfficiency

#Done, plot
h_numHits.Draw()
raw_input("Press Enter to continue...")

