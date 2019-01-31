import requests
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('file', help='Name of file to write output data.',
                    type=str, nargs='?', default='cards_data.json')
parser.add_argument('-v', '--verbose', help='Print progress messages.',
                    action='store_true')
args = parser.parse_args()

BASE_URL = 'https://api.magicthegathering.io/v1/'
CARDS_URL = BASE_URL + 'cards'
FORMATS_URL = BASE_URL + 'formats'
SETS_URL = BASE_URL + 'sets'
SUBTYPES_URL = BASE_URL + 'subtypes'
SUPERTYPES_URL = BASE_URL + 'supertypes'
TYPES_URL = BASE_URL + 'types'

if args.verbose:
    print('Retrieving cards data.')
first_cards_request = requests.get(CARDS_URL)
page_size = int(first_cards_request.headers['Page-Size'])
total_count = int(first_cards_request.headers['Total-Count'])
num_pages = total_count // page_size
if total_count % page_size > 0:
    num_pages += 1
cards = list(None for _ in range(total_count))
first_cards_page = first_cards_request.json()['cards']
for i in [x for x in range(len(first_cards_page))]:
    cards[i] = first_cards_page[i]
if args.verbose:
    print(f'Retrieving data for {total_count} cards.')
for page_num in range(1, num_pages):
    url_for_page = CARDS_URL + f'?page={page_num + 1}'
    if args.verbose:
        print(f'Retrieving page {page_num + 1} of {num_pages}.')
    cards_request = requests.get(url_for_page)
    cards_page = cards_request.json()['cards']
    for i in [x for x in range(len(cards_page))]:
        cards[i+page_num*page_size] = cards_page[i]

if args.verbose:
    print('Retrieving formats data.')
formats_request = requests.get(FORMATS_URL)
formats = formats_request.json()['formats']
if args.verbose:
    print('Formats data retrieved.')

if args.verbose:
    print('Retrieving sets data.')
sets_request = requests.get(SETS_URL)
sets = sets_request.json()['sets']
if args.verbose:
    print('Sets data retrieved.')

if args.verbose:
    print('Retrieving subtypes data.')
subtypes_request = requests.get(SUBTYPES_URL)
subtypes = subtypes_request.json()['subtypes']
if args.verbose:
    print('Subtypes data retrieved.')

if args.verbose:
    print('Retrieving supertypes data.')
supertypes_request = requests.get(SUPERTYPES_URL)
supertypes = supertypes_request.json()['supertypes']
if args.verbose:
    print('Supertypes data retrieved.')

if args.verbose:
    print('Retrieving types data.')
types_request = requests.get(TYPES_URL)
types = types_request.json()['types']
if args.verbose:
    print('Types data retrieved.')

output = dict()
output['cards'] = cards
output['formats'] = formats
output['sets'] = sets
output['subtypes'] = subtypes
output['supertypes'] = supertypes
output['types'] = types

if args.verbose:
    print('Writing data to file.')
with open(args.file, 'w') as f:
    json.dump(output,f)
