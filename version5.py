import json
import numpy as np
from scipy import stats
import networkx as nx 
import matplotlib.pyplot as plt
nameToIndex = {}
indexToName = {}
specieCount = 0
sampleToIndex = {}
sampleCount = 0
TIME_ROW = 0
NAME_ROW = 1
LARVAE_ROW = 2
THRESHOLD = 0.7

def network(dataFile, infoFile, networkFile):
    global specieCount 
    global sampleCount 
    #Parses file to count total number of distinct samples and species 
    file = open(dataFile)
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
    nameIndex = 0
    timeIndex = 0
    for i in data['table']['rows']:
        time = int(i[TIME_ROW][11:13] + i[TIME_ROW][14:16] + i[TIME_ROW][17:19])
        name = i[NAME_ROW]
        larvaeCount = i[LARVAE_ROW]
        nameIndex = nameToIndex[name]
        timeIndex = sampleToIndex[time]
        #Add larvae counts to matrix
        matrixCount[timeIndex][nameIndex] = larvaeCount
    #Get adjacency matrix
    matrixAd = correlate(matrixCount)
    #Create network from adjacency matrix
    graph(matrixAd, infoFile, networkFile) 

def correlate(counts):
    #Creates adjacency matrix 
    adjacency = np.zeros((specieCount, specieCount), float)
    for i in range(specieCount):
        for j in range(specieCount):
            if j > i:
                adjacency[i][j] = stats.spearmanr(counts[:, i], counts[:, j])[0]
    return adjacency 

def graph(matrixAd, dataFile, imageFile):
    #Creates graph with edges whose |edge weight| > minimum threshold 
    g = nx.Graph()
    for i in range(specieCount): 
        #Add all nodes (unqiue species)
        g.add_node(str(i) + ":" + indexToName[i])
        for j in range(specieCount):
            #Add edges if |correlation| between species is greater than chosen threshold  
            if j > i and (matrixAd[i][j] > THRESHOLD or matrixAd[i][j] < -1*THRESHOLD): 
                g.add_edge(str(i) + ": " + indexToName[i], str(j) + ": " + indexToName[j], weight = matrixAd[i][j])
    pos = nx.spring_layout(g, k= 0.11, iterations=12)
    nodeLabels = {n: n.partition(':')[0] for n in g.nodes}
    nx.draw_networkx_nodes(g, pos, node_size = 50)
    nx.draw_networkx_labels(g, pos, font_size = 8, labels=nodeLabels)
    nx.draw_networkx_edges(g, pos)
    outputFile = open(dataFile, 'w')
    #Prints a key that maps the node numbers of the network to the species name to info file
    print("Key for network nodes:", file=outputFile)
    print(indexToName, file=outputFile)
    print("", file=outputFile)
    #Prints the edge list of the network to the info file 
    print("Edge list for network:", file=outputFile)
    outputFile.close()
    outputFile = open(dataFile, 'ab')
    nx.write_weighted_edgelist(g, outputFile, delimiter=', ')
    outputFile.close()
    #Saves network to the file specified 
    plt.savefig(imageFile)

def main():
    #Create networks 
    network("2015data.json", "2015networkinfo", "2015network.png")
    #network(input_data_file, output_network_info_file, output_network_file)

#Call to main 
main() 
 
