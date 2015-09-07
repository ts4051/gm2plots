from ROOT import TFile, TDirectory, gROOT, gStyle, TCanvas, TTree, TF1, TProfile, TH1F, TH2F, TGraph, Double
from sys import exit

#
# Function to open a file
#

def openFile(fileName):

  rootFile = TFile(fileName, 'READ')
  if (rootFile.IsOpen == False): 
    print "ERROR: ROOT file",fileName,"opening failed"
    exit(-1)

  return rootFile


#
# Function to get object from file
#

def getFromFile(rootFile,objectPath):

  #Check file
  if (rootFile.IsOpen == False): 
    print "ERROR: Could not open ROOT file when searching for '",objectPath,"'"
    exit(-1)

  #Get object
  obj = rootFile.Get(objectPath)
  if not obj : 
    print "Error getting '",objectPath,"'"
    exit(-1)

  return obj

