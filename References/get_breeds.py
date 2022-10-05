import pokebase as pb
import requests
import time

t1 = time.time()

language = 'en'
breeds = requests.get('https://pokeapi.co/api/v2/pokemon-species/?limit=898')
breeds = breeds.json()

with open('pokemon_breeds.dat', 'w', encoding='utf-8') as file:
    num = 0

    for mon in breeds['results']:
        breed = requests.get(mon['url'])
        breed = breed.json()
        for name in breed['names']:
            if name['language']['name'] == language:
                file.write(f'{name["name"]} {num + 1}\n')
                break
        num += 1


t2 = time.time()
print(t2-t1)

