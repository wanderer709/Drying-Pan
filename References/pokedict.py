pokedict = {}

with open('pokemon_breeds.dat', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        end_of_breed_index = line.rfind(' ')
        pokedict[line[0:end_of_breed_index]] = line[end_of_breed_index+1:-1]

# print(pokedict)
