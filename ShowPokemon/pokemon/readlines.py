import os

with open('pokemon_types.dat', 'r', encoding='utf-8') as f:
    types_list = f.readlines()
types_pics_list = []
for types in types_list:
    types_pics_list.append(f'media/types/{types[:-1].lower()}')
print(types_pics_list)
