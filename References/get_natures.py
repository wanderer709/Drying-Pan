import pokebase as pb
import time

t1 = time.time()

language = 'en'

with open('pokemon_natures.dat', 'w', encoding='utf-8') as file:
    num = 1

    while True:
        try:
            for nature in pb.nature(num).names:
                if nature.language.name == language:
                    file.write(nature.name + '\n')
            num += 1
        except:
            break

t2 = time.time()
print(t2-t1)
