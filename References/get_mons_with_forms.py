import requests

response = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=1126')
pokemon = response.json()['results']

breeds = set()
multiple_forms = set()
multiple_names = set()

for mon in pokemon:
    breed = requests.get(mon['url'])
    breed_name = breed.json()['name']
    breed = breed.json()['species']['name']
    breeds_len_before = len(breeds)
    breeds.add(breed)
    # print(breeds)
    if len(breeds) == breeds_len_before:
        # print(breed)
        multiple_forms.add(breed)
        multiple_names.add(breed_name)

with open('pokemon_with_multiple_forms.dat', 'w', encoding='utf-8') as file:
    for breed in multiple_forms:
        file.write(breed + '\n')

with open('multiple_form_names.dat', 'w', encoding='utf-8') as file:
    for name in multiple_names:
        file.write(name + '\n')

# print(multiple_forms)





# mon = requests.get(mons.json()['results'][0]['url'])
# print(mon.json()['name'])
