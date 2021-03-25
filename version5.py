import json
import numpy as np
from scipy import stats 
nameToIndex = {}
indexToName = {}
specieCount = 0
sampleToIndex = {}
sampleCount = 0
TIME_ROW = 10
NAME_ROW = 11
LARVAE_ROW = 16

def network(fileName):
    global specieCount 
    global sampleCount 
    #Parses file to count total number of distinct samples and species 
    file = open(fileName)
    data = json.load(file)
    for i in data['table']['rows']:
        time = int(i[TIME_ROW][11:13] + i[TIME_ROW][14:16] + i[TIME_ROW][17:19])
        name = i[NAME_ROW]
        #Count total number of species and assign them index values
        if(name not in nameToIndex):
            nameToIndex[name] = specieCount
            indexToName[specieCount] = name
            specieCount = specieCount + 1
        #Count total number of samples and assign them index values
        if(time not in sampleToIndex):
            sampleToIndex[time] = sampleCount
            sampleCount = sampleCount + 1
    file.close()
    #Parses data to create matrix of larvae counts with sampleCount rows and specieCount columns 
    matrixCount = np.zeros((sampleCount, specieCount), float)
    for i in data['table']['rows']:
        time = int(i[TIME_ROW][11:13] + i[TIME_ROW][14:16] + i[TIME_ROW][17:19])
        name = i[NAME_ROW]
        larvaeCount = i[LARVAE_ROW]
        nameIndex = 0
        timeIndex = 0
        nameIndex = nameToIndex[name]
        timeIndex = sampleToIndex[time]
        #Add larvae counts to matrix
        matrixCount[timeIndex][nameIndex] = larvaeCount
    print(matrixCount)
    sourceFile = open('test', 'w')
    print(matrixCount, file = sourceFile)
    sourceFile.close()
    #Get adjacency matrix
    matrixAd = correlate(matrixCount)
    #Create network from adjacency matrix 


def correlate(counts):
    sourceFile = open('test', 'w')
    #print(matrixCount, file = sourceFile)
    #sourceFile = open('test', 'w')
    #print(matrixCount, file = sourceFile)
    #sourceFile.close()
    #Creates adjacency matrix 
    adjacency = np.zeros((specieCount, specieCount), float)
    i = 0
    j = 0
    for i in range(specieCount):
        for j in range(specieCount):
            if j > i:
                adjacency[i][j] = stats.spearmanr(counts[:, i], counts[:, j])[0]
    print(adjacency)
    sourceFile = open('test', 'w')
    print(adjacency, file = sourceFile)
    sourceFile.close()
    return adjacency 

def main():
    #Create networks 
    network("2015_data.json")
    #network("")

#Call to main 
main() 
 
