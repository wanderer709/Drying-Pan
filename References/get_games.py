import pokebase as pb
import time

t1 = time.time()

language = 'en'

with open('pokemon_games.dat', 'w', encoding='utf-8') as file:
    num = 1

    while True:
        try:
            for game in pb.version(num).names:
                if game.language.name == language:
                    file.write(game.name + '\n')
            num += 1
        except:
            break

t2 = time.time()
print(t2-t1)

