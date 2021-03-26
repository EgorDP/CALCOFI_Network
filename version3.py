#%%
import json
import numpy as np
import networkx as nx
import matplotlib as mt
import matplotlib.pyplot as plt
from scipy import stats

# Visuals
NAMES_IN_PERIODS = False

# Rows Of Data
DATA_RANGE = 50

# Debug Info
debug_bool = True

# Variables set to column they appear in the datashet
LARVAE = 16   
TIME = 10               
SCIENTIFIC_NAME = 11    

animal_dict = {}        # Dictionary of (animals, index) for matrix
time1 = []              # Time  0:01 -  6:00
time2 = []              # Time  6:01 - 12:00
time3 = []              # Time 12:01 - 18:00
time4 = []              # Time 18:01 -  0:00
time1_times = {}        # Dictionary of (times, index) for matrix
time2_times = {}
time3_times = {}
time4_times = {}
animal1 = {}
animal2 = {}
animal3 = {}
animal4 = {}
time1_count, time2_count, time3_count, time4_count = 0,0,0,0 # Counts of specific times in the time periods
matrix1, matrix2, matrix3, matrix4 = None,None,None,None
animal_count = 0

def debug(s):
    if(debug_bool):
        print(s)

# Class to store animal information, one instance for each sample an animal appears in
class Animal:
    def __init__(self, name, time, larvae):
        self.name = name
        self.time = time
        self.larvae = larvae        

def processTime(str):
    ''' Process times into a numerical format e.g '13:04' -> 1304, '00:02' -> 2 '''
    first = 0
    second = 0
    if(str[0] == '0'):    #If time starts with 0 in leading hour's place, get only second place
        first = int(str[1])
    else:
        first = int(str[0:2])
    if(str[-2] == '0'):   #If time ends with 0 in the leading minute's place, get only second place
        second = int(str[-1])
    else:
        second = int(str[-2:-1])
    return first * 100 + second


def processDate(str):
    ''' Process data into a numberical format
    \n e.g. 04/03 -> 4 * 1000000 + 3 * 10000 = 4030000
    \n Combined with output of processTime(), their sum will be: 04/03 at 44:12 -> 4000000 + 30000 + 4400 + 12 = 4034412'''
    first = 0
    second = 0
    if(str[0] == '0'):    #If date starts with 0 in leading month's place, get only second place
        first = int(str[1])
    else:
        first = int(str[0:2])
    if(str[3] == '0'):   #If date ends with 0 in the leading date's place, get only second place
        second = int(str[4])
    else:
        second = int(str[3:4])
    return (first * 1000000) + (second * 10000)

def create_animal_dict(fileName) -> dict:
    ''' Partitions the data from a JSON file into time periods
        \nCalls the appropriate methods to convert the information in the time periods
        to matrices representing animals vs samples (each value is the amount of larvae
        per 10 meters in a sample)
        \nCalls correlation methods and subsequently visualization methods on these matrices
    ''' 
    file = open(fileName)                         # Open buffer
    data = json.load(file)

    global time1 
    global time2 
    global time3 
    global time4
    global time1_times 
    global time2_times 
    global time3_times
    global time4_times 
    global time1_count
    global time2_count
    global time3_count
    global time4_count
    time1_times,time2_times,time3_times,time4_times = 0,0,0,0
    time1 = []
    time2 = []
    time3 = []
    time4 = []
    time1_times = {}
    time2_times = {}
    time3_times = {}
    time4_times = {}
    global animal_dict
    animal_dict = {}
    global animal_count                       # Put the count of animals into global scope
    animal_count = 0
    animal1_count = 0
    animal2_count = 0
    animal3_count = 0
    animal4_count = 0
    limit = 0                                  # Limits the amount of data used                            

    for i in data['table']['rows']:
        name = i[SCIENTIFIC_NAME]
        time = processTime(i[TIME][-9:-4])
        date = processDate(i[TIME][5:10])
        larvae = i[LARVAE]
        animal = Animal(name = name, time = time + date, larvae = larvae)
        if time < 600:
                time1.append(animal)   
                time = time + date   # Combine time and date to get unique sample location ID
                if time not in time1_times:
                    time1_times[time] = time1_count  # Set the new time to a new index (for matrix computations)
                    time1_count = time1_count + 1
                if name not in animal1:              # Keep track of the animals in this time period only
                    animal1[name] = animal1_count 
                    animal1_count = animal1_count + 1
        elif time < 1200:           # Repeat actions above, now for time period 2
                time2.append(animal) 
                time = time + date 
                if time not in time2_times:
                    time2_times[time] = time2_count  
                    time2_count = time2_count + 1
                if name not in animal2:
                    animal2[name] = animal2_count 
                    animal2_count = animal2_count + 1
        elif time < 1800:
                time3.append(animal)
                time = time + date 
                if time not in time3_times:
                    time3_times[time] = time3_count  
                    time3_count = time3_count + 1
                if name not in animal3:
                    animal3[name] = animal3_count 
                    animal3_count = animal3_count + 1
        elif time < 2400:
                time4.append(animal)
                time = time + date 
                if time not in time4_times:
                    time4_times[time] = time4_count  
                    time4_count = time4_count + 1
                if name not in animal4:
                    animal4[name] = animal4_count 
                    animal4_count = animal4_count + 1

        if name not in animal_dict.keys():
           animal_dict[name] = animal_count
           animal_count = animal_count + 1
        limit = limit + 1
        if limit > DATA_RANGE:
            break 
    if(NAMES_IN_PERIODS):  # Display the animals in the periods if necessary
        print("Time 1")
        for i in time1:
            print(i.name)
        print("Time 2")
        for i in time2:
            print(i.name)
        print("Time 3")
        for i in time3:
            print(i.name)
        print("Time 4")
        for i in time4:
            print(i.name)
    file.close() # Close buffer
    print()
    #print("Sample count: " + str(time1_count + time2_count + time3_count + time4_count) + ", matrix should have this many rows")
 
    matrix1= time_to_matrixAnimals(time1, time1_times, animal1)
    #matrix2 = time_to_matrix(time2, time2_times)
    #matrix3 = time_to_matrix(time3, time3_times)
    #matrix4 = time_to_matrix(time4, time4_times)
    matrix1_correlated = correlate(matrix1, animal1)
    createGraph(matrix1_correlated)
    #correlate(matrix2)
    #correlate(matrix3)
    #correlate(matrix4)

# @param time : time period with all animal objects that appear during that period
# @param time_times : all specific times within a time period
def time_to_matrix(time, time_times, animal):
    # Matrix for x axis: animals, y  axis: sample (categorized by the time)
    # Creates a list containing (Samples) amount of lists, each with (animal_count) items
    w,h  = len(animal), len(time_times)
    Matrix = [[0 for x in range(w)] for y in range(h)] 

    for i in time:
        y = animal_dict[i.name]    # Get index corresponding to animal name
        x = time_times[i.time]     # Get index correspondiing to animal time in the sample
        Matrix[x][y] = i.larvae

    for i in Matrix:
        print(i)
    return Matrix

# Same as time_to_matrix except organized by species and not samples
def time_to_matrixAnimals(time, time_times, animal):
    #A = np.arrange(20).reshape(4,5)
    # So for each entry in time, we get its name and it's time. Use the dictionary to compute where to find it in the matrix
        #time_times.sort()

    # Matrix for x axis: animals, y  axis: sample (categorized by the time)
    # Creates a list containing (Samples) amount of lists, each with (animal_count) items
    print("Dict is: " + str(animal))
    w,h  = len(time_times), len(animal)
    Matrix = [[0 for x in range(w)] for y in range(h)] 

    for i in time:
        x = animal[i.name]         # Get index corresponding to animal name
        y = time_times[i.time]     # Get index correspondiing to animal time in the sample
        Matrix[x][y] = i.larvae

    for i in Matrix:
        print(i)
    return Matrix

# Correlate specie's larvae counts over different sample times 
def correlate(matrix, animal):
    print(1)
    if len(matrix) < 2:  # If there is only 1 animal, no correlation can exist
        return -1

    a = np.array(matrix)
    b = np.corrcoef(a)
    for i in b:
        print(i)
        print()
    
    i = 0
    #list_total = []
    #for b in b:
        #list_total.append(b)
    for key in animal:   # Update the animal dict with correlation lists (for use in creating the network)
        animal[key] = b[i]
        i = i+1
    for key,value in animal.items():
        print(key, ' : ', value)
    return animal
        
def createGraph(matrix):
    #G = nx.from_dict_of_lists(matrix)  # TODO: Add a graph constructor
    #G = nx.Graph(matrix)
    #G2 = nx.adjacency_matrix(matrix)
    
    G = nx.Graph()
    nodes = matrix.keys()
    #edges = [(j,k,w) for j in matrix.keys() for k in matrix.keys() for w in matrix[j]]
    
    list_anim = []
    for key in matrix:
        list_anim.append(key)

    for key in matrix:
        index = 0
        for i in matrix[key]:
            if(i>0):
                G.add_edge(key, list_anim[index],weight = round(i,2) )
            index = index + 1
    G.add_nodes_from(nodes)
    #G.add_weighted_edges_from(edges)

    #pos = nx.spring_layout(G, k=0.20, iterations=20)
    pos = nx.shell_layout(G) # Create positions of all nodes and save them
    #nx.draw(G, pos, with_labels=True) # Draw the graph according to node positions
    #nx.draw_networkx_nodes(G,pos,node_size = 100)

    labels = nx.get_edge_attributes(G,'weight') # Create edge labels
    #plt.figure(3,figsize=(24,24)) 
    nx.draw_networkx(G,pos,node_size= 50, font_size = 8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size= 6) # Draw edge labels according to node positions
    

    plt.show()
    
def main(): 
    create_animal_dict("2015_data.json")


# Call to main 
main()
# %%
