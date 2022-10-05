import pokebase as pb
import time

t1 = time.time()

language = 'en'

with open('pokemon_items.dat', 'w', encoding='utf-8') as file:
    num = 1

    while True:
        try:
            for item in pb.item(num).names:
                if item.language.name == language:
                    file.write(item.name + '\n')
            num += 1
        except:
            break

t2 = time.time()
print(t2-t1)

