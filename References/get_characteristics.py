import pokebase as pb
import time

t1 = time.time()

language = 'en'

with open('pokemon_characteristics.dat', 'w', encoding='utf-8') as file:
    num = 1

    while True:
        try:
            for characteristic in pb.characteristic(num).descriptions:
                if characteristic.language.name == language:
                    file.write(characteristic.description + '\n')
            num += 1
        except:
            break

t2 = time.time()
print(t2-t1)
