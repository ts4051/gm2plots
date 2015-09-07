from ROOT import TFile, TDirectory, gROOT, gStyle, TCanvas, TTree, TF1, TProfile, TH1F, TH2F, TGraph, Double
from sys import exit
import os

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



#
# Function to group objects of same in different files into a single file
#

#ROOT doesn't like superimposing onto same plot from different files, so crate a tmp one with all the files you need

def groupObjectsFromDiffFiles(tmpFileName,filePaths,objectPath): #Must provide dict with key for files (need something to discriminate in new name)

  #Create the tmp file
  tmpFile = TFile.Open(tmpFileName,'RECREATE')
  tmpFile.Close()

  #Loop over files
  clonePaths = dict()
  for key, filePath in filePaths.iteritems():

    #Open input file
    rootFile = openFile(filePath)

    #Get object
    obj = getFromFile(rootFile,objectPath)

    #Clone object into tmp file with new name (uses key)
    tmpFile = TFile.Open(tmpFileName,'UPDATE') #Open for modification, don't recreate
    clonePaths[key] = os.path.basename(objectPath)+'_'+str(key)
    print clonePaths[key]
    clone = obj.Clone(clonePaths[key])
    clone.Write()
    tmpFile.Close()

    #Close input file now done with it
    rootFile.Close()

  return clonePaths


