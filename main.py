import json

data = None
ROWLATITUDE = 7   # Column number that latitude value is located in 
ROWLARVAE = 16   
debug_bool = True

# 
# Algorithm:
# TODO: Put in algorithm steps
# TODO: Create adjacency matrix for weightd edges on the graph
#

def debug(s):
    if(debug_bool):
        print(s)

class Animal:
    def __init__(self, latitude, larvae_amount):
        super().__init__()
        self.latitude = latitude
        self.name = larvae_amount

def data_partition_groups(fileName) -> dict:
    ''' Partition the data from a JSON file into animal groups based on location ''' 
    file = open(fileName)                         # Open buffer
    data = json.load(file)

    species_location = []                         # Temp list with all species in a location
    animal_group = []                             # Group animals by their location
    latitude_temp = None
    first = data['table']['rows'][0]              # Temp set to first animal 
    animal_group.append(Animal(latitude=first[ROWLATITUDE], larvae_amount=first[ROWLARVAE]) )

    temp = 0                                      # REMOVE: testing variable for now to only get 5 values

    length = len(data['table']['rows'])
    for i in range(1, length):
        position = data['table']['rows'][i]       # Add the animal at the current position
        animal_temp = Animal(latitude=position[ROWLATITUDE], larvae_amount=position[ROWLARVAE])
        debug(animal_temp.latitude)

        if(animal_group[0].latitude != animal_temp.latitude):     # Begin new animal group by location 
            correlate(animal_group)               # Correlate the previous animal_group
            animal_group.clear()                  # Clear the animal_group for species at new location

        animal_group.append(animal_temp)   
        temp = temp + 1
        if temp > 5:
            break

    file.close()                                  # Close buffer
        
# TODO: Find out if this is necessary?
def init_hash_map(data):
    ''' Hash map for unique locations of species ''' 
    def sort_func(arr):
        return arr['latitude']
    data.sort(key = sort_func)

# TODO: Implement C(n,2) correlations per array, update adjacency matrix
def correlate(list):
    debug("Correlate called")
    temp = None

def main():
    data_partition_groups("2015_data.json")

# Call to main 
main()