import requests
import psycopg2
import argparse
import json
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', help='Print progress messages.',
                    action='store_true')
args = parser.parse_args()

BASE_URL = 'https://api.magicthegathering.io/v1/'
CARDS_URL = BASE_URL + 'cards'
FORMATS_URL = BASE_URL + 'formats'
SETS_URL = BASE_URL + 'sets'
SUBTYPES_URL = BASE_URL + 'subtypes'
SUPERTYPES_URL = BASE_URL + 'supertypes'
TYPES_URL = BASE_URL + 'types'
DB_CONN_STRING = 'dbname=cardconf'

if args.verbose:
    print('Retrieving cards data.')
first_cards_request = requests.get(CARDS_URL)
page_size = first_cards_request.headers['Page-Size']
total_count = first_cards_request.headers['Total-Count']
num_pages = total_count // page_size
if total_count % page_size > 0:
    num_pages += 1
card_pages = list(None for _ in range(num_pages))
card_pages[0] = first_cards_request.json()['cards']
for page_num in range(1, num_pages):
    url_for_page = CARDS_URL + f'?page={page_num + 1}'
    cards_request = requests.get(url_for_page)
    card_pages[page_num] = cards_request.json()['cards']
if args.verbose:
    print(f'{num_pages} pages retrieved.')

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
supertypes = subtypes_request.json()['supertypes']
if args.verbose:
    print('Supertypes data retrieved.')

if args.verbose:
    print('Retrieving types data.')
types_request = requests.get(TYPES_URL)
types = types_request.json()['types']
if args.verbose:
    print('Types data retrieved.')

if args.verbose:
    print('Opening database connection.')
db_conn = psycopg2.connect(DB_CONN_STRING)
db_cursor = db_conn.cursor()
if args.verbose:
    print('Refreshing card data staging tables.')
db_cursor.execute('DROP TABLE IF EXISTS cards_staging')
db_cursor.execute('''CREATE TABLE public.cards_staging (
    name character varying(400),
    layout character varying(50),
    cmc integer,
    type character varying(200),
    supertypes jsonb,
    types jsonb,
    subtypes jsonb,
    rarity character varying(50),
    set character varying(10),
    set_name character varying(100),
    text text,
    flavor text,
    artist character varying(100),
    number character varying(20),
    power character varying(20),
    toughness character varying(20),
    loyalty character varying(20),
    names jsonb,
    mana_cost character varying(200),
    variations jsonb,
    image_url character varying(2000),
    watermark character varying(100),
    border character varying(20),
    timeshifted boolean,
    hand integer,
    life integer,
    reserved boolean,
    release_date character varying(50),
    starter boolean,
    rulings jsonb,
    foreign_names jsonb,
    printings jsonb,
    original_text text,
    original_type character varying(200),
    legalities jsonb,
    source text,
    multiverse_id integer
)''')
db_cursor.execute('DROP TABLE IF EXISTS cards_color_staging')
db_cursor.execute('''CREATE TABLE public.cards_color_staging (
    name character varying(400),
    color character varying(20)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_color_identity_staging')
db_cursor.execute('''CREATE TABLE public.cards_color_identity_staging (
    name character varying(400),
    color character varying(20)
    )''')

for card_page in card_pages:
    cards_staging_args = [None for _ in range(len(card_page))]
    color_staging_args = deque()
    color_identity_staging_args = deque()
    for card_index in range(len(card_page)):
        name_arg = card_page[card_index]['name']
        layout_arg = card_page[card_index]['layout']
        cmc_arg = card_page[card_index]['cmc']
        type_arg = card_page[card_index]['type']
        supertypes_arg = json.dumps(card_page[card_index]['supertypes'])
        types_arg = json.dumps(card_page[card_index]['types'])
        subtypes_arg = json.dumps(card_page[card_index]['subtypes'])
        rarity_arg = card_page[card_index]['rarity']
        set_arg = card_page[card_index]['set']
        set_name_arg = card_page[card_index]['setName']
        text_arg = card_page[card_index]['text']
        flavor_arg = card_page[card_index]['flavor']
        artist_arg = card_page[card_index]['artist']
        number_arg = card_page[card_index]['number']
        power_arg = card_page[card_index]['power']
        toughness_arg = card_page[card_index]['toughness']
        loyalty_arg = card_page[card_index]['loyalty']
        names_arg = json.dumps(card_page[card_index]['names'])
        mana_cost_arg = card_page[card_index]['manaCost']
        variations_arg = json.dumps(card_page[card_index]['variations'])
        image_url_arg = card_page[card_index]['imageUrl']
        watermark_arg = card_page[card_index]['watermark']
        border_arg = card_page[card_index]['border']
        timeshifted_arg = card_page[card_index]['timeshifted']
        hand_arg = card_page[card_index]['hand']
        life_arg = card_page[card_index]['life']
        reserved_arg = card_page[card_index]['reserved']
        release_date_arg = card_page[card_index]['releaseDate']
        starter_arg = card_page[card_index]['starter']
        rulings_arg = json.dumps(card_page[card_index]['rulings'])
        foreign_names_arg = json.dumps(card_page[card_index]['foreignNames'])
        printings_arg = json.dumps(card_page[card_index]['printings'])
        original_text_arg = card_page[card_index]['originalText']
        original_type_arg = card_page[card_index]['originalType']
        legalities_arg = json.dumps(card_page[card_index]['legalities'])
        source_arg = card_page[card_index]['source']
        multiverse_id_arg = card_page[card_index]['multiverseId']
        cards_staging_args[card_index] = (name_arg, layout_arg, cmc_arg,
                                          type_arg, supertypes_arg, types_arg,
                                          subtypes_arg, rarity_arg, set_arg,
                                          set_name_arg, text_arg, flavor_arg,
                                          artist_arg, number_arg, power_arg,
                                          toughness_arg, loyalty_arg,
                                          names_arg, power_arg, toughness_arg,
                                          loyalty_arg, names_arg,
                                          mana_cost_arg, variations_arg,
                                          image_url_arg, watermark_arg,
                                          border_arg, timeshifted_arg,
                                          hand_arg, life_arg, reserved_arg,
                                          release_date_arg, starter_arg,
                                          rulings_arg, foreign_names_arg,
                                          printings_arg, original_text_arg,
                                          original_type_arg, legalities_arg,
                                          source_arg, multiverse_id_arg)
        # TODO: argument lists for color and color identity