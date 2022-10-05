import os

pokedict = {}
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'pokemon_breeds.dat')

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file.readlines():
        end_of_breed_index = line.rfind(' ')
        pokedict[line[0:end_of_breed_index]] = line[end_of_breed_index+1:-1]

# print(pokedict)
