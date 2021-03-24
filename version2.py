import json

animal_dict = {}        # Dictionary of species 
LATITUDE = 7            # Variables set to corresponding column they appear in the datashet
LARVAE = 16   
TIME = 10               
SCIENTIFIC_NAME = 11    
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
    def __init__(self, name, sample):
        super().__init__()
        self.samples = []
        self.samples.append(sample)
    def append(self, sample):
        self.samples.append(sample)

class Sample:
    def __init__(self, time, latitude, larvae_amount):
        super().__init__()
        self.time = time
        self.latitude = latitude
        self.larvae_amount = larvae_amount

def create_animal_list(fileName) -> dict:
    ''' Partition the data from a JSON file into animal groups based on location ''' 
    file = open(fileName)                         # Open buffer
    data = json.load(file)


    animal_count = 0                             # Count amount of unique animals

    temp = 0                                      # REMOVE: testing variable for now to only get 5 values

    for i in data['table']['rows']:
        name = i[SCIENTIFIC_NAME]
        time = i[TIME]
        latitude = i[LATITUDE]
        larvae_amount = i[LARVAE]
        sample = Sample(time = time, latitude = latitude, larvae_amount = larvae_amount)
        if(name in animal_dict):                # Animal in the dictionary, append data
            updated_animal = animal_dict[name].append(sample)    
            animal_dict[name] = updated_animal  # Update animal with another Sample
        else:                                    # Animal is NOT in the dictionary, create and append
            animal = Animal(name = name,sample = sample)
            animal_dict[name] = animal
        temp = temp + 1
        if temp > 5:
            break      
    
    for i in animal_dict:
        print("Animal: " + i + " Time: " + animal_dict[i].samples[0].time)
    file.close()                                  # Close buffer
        

# TODO: Implement C(n,2) correlations per array, update adjacency matrix
def correlate(list):
    debug("Correlate called")


def main():
    create_animal_list("2015_data.json")

# Call to main 
main()