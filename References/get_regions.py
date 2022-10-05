import pokebase as pb
import time

t1 = time.time()

language = 'en'

with open('pokemon_regions.dat', 'w', encoding='utf-8') as file:
    num = 1

    while pb.generation(num):
        file.write(pb.generation(num).main_region.name.capitalize() + '\n')
        num += 1

t2 = time.time()
print(t2-t1)

