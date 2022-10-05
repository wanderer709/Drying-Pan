import pokebase as pb
import time

t1 = time.time()

language = 'en'

with open('pokemon_moves.dat', 'w', encoding='utf-8') as file:
    num = 1

    while True:
        try:
            for move in pb.move(num).names:
                if move.language.name == language:
                    file.write(move.name + '\n')
            num += 1
        except:
            break

t2 = time.time()
print(t2-t1)

