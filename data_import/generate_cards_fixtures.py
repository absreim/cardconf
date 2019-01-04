import requests
import psycopg2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', help='Print progress messages.',
                    action='store_true')
args = parser.parse_args()

CARDS_URL = 'https://api.magicthegathering.io/v1/cards'
FORMATS_URL = 'https://api.magicthegathering.io/v1/formats'
SETS_URL = 'https://api.magicthegathering.io/v1/sets'
SUBTYPES_URL = 'https://api.magicthegathering.io/v1/subtypes'
SUPERTYPES_URL = 'https://api.magicthegathering.io/v1/supertypes'
TYPES_URL = 'https://api.magicthegathering.io/v1/types'
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

db_conn = psycopg2.connect(DB_CONN_STRING)
db_cursor = db_conn.cursor()
db_cursor.execute('DROP TABLE IF EXISTS cards_staging')
db_cursor.execute('''CREATE TABLE public.cards_staging (
    name character varying(400),
    layout character varying(50),
    cmc integer,
    colors jsonb,
    color_identity jsonb,
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
