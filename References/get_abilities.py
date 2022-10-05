import pokebase as pb
import time

t1 = time.time()

language = 'en'

with open('pokemon_abilities.dat', 'w', encoding='utf-8') as file:
    num = 1

    while True:
        try:
            for ability in pb.ability(num).names:
                if ability.language.name == language:
                    file.write(ability.name + '\n')
            num += 1
        except:
            break

t2 = time.time()
print(t2-t1)

