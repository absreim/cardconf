import psycopg2
import argparse
import json
from collections import deque
from psycopg2.extras import execute_batch

DB_CONN_STRING = 'dbname=cardconf'

parser = argparse.ArgumentParser()
parser.add_argument('file', help='Path to file containing cards data.',
                    type=str, default='cards_data.json')
parser.add_argument('--verbose', help='Print progress messages.',
                    action='store_true')
args = parser.parse_args()

if args.verbose:
    print('Loading data from file.')
with open(args.file,'r') as f:
    data = json.load(f)

if args.verbose:
    print('Opening database connection.')
db_conn = psycopg2.connect(DB_CONN_STRING)
db_cursor = db_conn.cursor()

if args.verbose:
    print('Refreshing card data staging tables.')
db_cursor.execute('DROP TABLE IF EXISTS cards_staging')
db_cursor.execute('''CREATE TABLE cards_staging (
    name character varying(400),
    layout character varying(50),
    cmc integer,
    type character varying(200),
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
    mana_cost character varying(200),
    image_url character varying(2000),
    watermark character varying(100),
    border character varying(20),
    timeshifted boolean,
    hand integer,
    life integer,
    reserved boolean,
    release_date character varying(50),
    starter boolean,
    original_text text,
    original_type character varying(200),
    source text,
    multiverse_id integer,
    id varchar(100)
)''')
db_cursor.execute('DROP TABLE IF EXISTS cards_color_staging')
db_cursor.execute('''CREATE TABLE cards_color_staging (
    name character varying(400),
    color character varying(20)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_color_identity_staging')
db_cursor.execute('''CREATE TABLE cards_color_identity_staging (
    name character varying(400),
    color character varying(20)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_supertypes_staging')
db_cursor.execute('''CREATE TABLE cards_supertypes_staging (
    name varchar(400),
    supertype varchar(50)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_types_staging')
db_cursor.execute('''CREATE TABLE cards_types_staging (
    name varchar(400),
    type varchar(50)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_subtypes_staging')
db_cursor.execute('''CREATE TABLE cards_subtypes_staging (
    name varchar(400),
    subtype varchar(50)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_names_staging')
db_cursor.execute('''CREATE TABLE cards_names_staging (
    name varchar(400),
    alt_name varchar(400)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_variations_staging')
db_cursor.execute('''CREATE TABLE cards_variations_staging (
    name varchar(400),
    id varchar(100)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_rulings_staging')
db_cursor.execute('''CREATE TABLE cards_rulings_staging (
    name varchar(400),
    date varchar(20),
    text text
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_foreign_names_staging')
db_cursor.execute('''CREATE TABLE cards_foreign_names_staging (
    name varchar(400),
    text text,
    flavor text,
    image_url varchar(2000),
    language varchar(50),
    multiverse_id integer
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_printings_staging')
db_cursor.execute('''CREATE TABLE cards_printings_staging (
    name varchar(400),
    set varchar(10)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_legalities_staging')
db_cursor.execute('''CREATE TABLE cards_legalities_staging (
    name varchar(400),
    format varchar(50),
    legality varchar(50)
    )''')

cards = data['cards']
cards_args = [None for _ in range(len(cards))]
cards_color_args = deque()
cards_color_identity_args = deque()
cards_supertypes_args = deque()
cards_types_args = deque()
cards_subtypes_args = deque()
cards_names_args = deque()
cards_variations_args = deque()
cards_rulings_args = deque()
cards_foreign_names_args = deque()
cards_printings_args = deque()
cards_legalities_args = deque()
for card_index in range(len(cards)):
    name_arg = cards[card_index]['name']
    layout_arg = cards[card_index]['layout'] if 'layout' in \
        cards[card_index] else ''
    cmc_arg = cards[card_index]['cmc'] if 'cmc' in \
        cards[card_index] else None
    type_arg = cards[card_index]['type'] if 'type' in \
        cards[card_index] else ''
    rarity_arg = cards[card_index]['rarity'] if 'rarity' in \
        cards[card_index] else ''
    set_arg = cards[card_index]['set'] if 'set' in \
        cards[card_index] else ''
    set_name_arg = cards[card_index]['setName'] if 'setName' in \
        cards[card_index] else ''
    text_arg = cards[card_index]['text'] if 'text' in \
        cards[card_index] else ''
    flavor_arg = cards[card_index]['flavor'] if 'flavor' in \
        cards[card_index] else ''
    artist_arg = cards[card_index]['artist'] if 'artist' in \
        cards[card_index] else ''
    number_arg = cards[card_index]['number'] if 'number' in \
        cards[card_index] else ''
    power_arg = cards[card_index]['power'] if 'power' in \
        cards[card_index] else ''
    toughness_arg = cards[card_index]['toughness'] if 'toughness' in \
        cards[card_index] else ''
    loyalty_arg = cards[card_index]['loyalty'] if 'loyalty' in \
        cards[card_index] else ''
    mana_cost_arg = cards[card_index]['manaCost'] if 'manaCost' in \
        cards[card_index] else ''
    image_url_arg = cards[card_index]['imageUrl'] if 'imageUrl' in \
        cards[card_index] else ''
    watermark_arg = cards[card_index]['watermark'] if 'watermark' in \
        cards[card_index] else ''
    border_arg = cards[card_index]['border'] if 'border' in \
        cards[card_index] else ''
    timeshifted_arg = cards[card_index]['timeshifted'] if \
        'timeshifted' in cards[card_index] else False
    hand_arg = cards[card_index]['hand'] if 'hand' in \
        cards[card_index] else None
    life_arg = cards[card_index]['life'] if 'life' in \
        cards[card_index] else None
    reserved_arg = cards[card_index]['reserved'] if 'reserved' in \
        cards[card_index] else False
    release_date_arg = cards[card_index]['releaseDate'] if \
        'releaseDate' in cards[card_index] else ''
    starter_arg = cards[card_index]['starter'] if 'stater' in \
        cards[card_index] else False
    original_text_arg = cards[card_index]['originalText'] if \
        'originalText' in cards[card_index] else ''
    original_type_arg = cards[card_index]['originalType'] if \
        'originalType' in cards[card_index] else ''
    source_arg = cards[card_index]['source'] if 'source' in \
        cards[card_index] else ''
    multiverse_id_arg = cards[card_index]['multiverseid'] if \
        'multiverseid' in cards[card_index] else None
    id_arg = cards[card_index]['id'] if 'id' in cards[card_index] else None
    cards_args[card_index] = (name_arg, layout_arg, cmc_arg,
        type_arg, rarity_arg, set_arg, set_name_arg, text_arg, flavor_arg,
        artist_arg, number_arg, power_arg, toughness_arg, loyalty_arg,
        mana_cost_arg, image_url_arg, watermark_arg,
        border_arg, timeshifted_arg, hand_arg, life_arg, reserved_arg,
        release_date_arg, starter_arg, original_text_arg, original_type_arg,
        source_arg, multiverse_id_arg, id_arg)
    # Name does not uniquely identify a card, but that is ok for the
    # purposes of the staging tables. The query that accesses the
    # staging tables should be written to distinctly select data
    # as appropriate.
    if 'colors' in cards[card_index]:
        for color in cards[card_index]['colors']:
            cards_color_args.append((name_arg, color))
    if 'colorIdentity' in cards[card_index]:
        for color in cards[card_index]['colorIdentity']:
            cards_color_identity_args.append((name_arg, color))
    if 'supertypes' in cards[card_index]:
        for supertype in cards[card_index]['supertypes']:
            cards_supertypes_args.append((name_arg, supertype))
    if 'types' in cards[card_index]:
        for type in cards[card_index]['types']:
            cards_types_args.append((name_arg, type))
    if 'subtypes' in cards[card_index]:
        for subtype in cards[card_index]['subtypes']:
            cards_subtypes_args.append((name_arg, subtype))
    if 'names' in cards[card_index]:
        for alt_name in cards[card_index]['names']:
            cards_names_args.append((name_arg, alt_name))
    if 'variations' in cards[card_index]:
        for id in cards[card_index]['variations']:
            cards_variations_args.append((name_arg, id))
    if 'rulings' in cards[card_index]:
        for ruling in cards[card_index]['rulings']:
            cards_rulings_args.append((name_arg, ruling['date'],
                                       ruling['text']))
    if 'foreignNames' in cards[card_index]:
        for foreign_name in cards[card_index]['foreignNames']:
            cards_foreign_names_args.append((name_arg, foreign_name['text'],
                foreign_name['flavor'], foreign_name['imageUrl'],
                foreign_name['language'], foreign_name['multiverseid']))
    if 'printings' in cards[card_index]:
        for printing in cards[card_index]['printings']:
            cards_printings_args.append((name_arg, printing))
    if 'legalities' in cards[card_index]:
        for legality in cards[card_index]['legalities']:
            cards_legalities_args.append((name_arg, legality['format'],
                                          legality['legality']))
execute_batch(db_cursor, ('INSERT INTO cards_staging (name, layout,'
    'cmc, type, rarity, set, set_name, text,'
    'flavor, artist, number, power, toughness, loyalty, mana_cost,'
    'image_url, watermark, border, timeshifted, hand, life,'
    'reserved, release_date, starter, original_text, original_type,'
    'source, multiverse_id, id) '
    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
    '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'), cards_args)
execute_batch(db_cursor, ('INSERT INTO cards_color_staging (name,'
    'color) VALUES (%s, %s)'),list(cards_color_args))
execute_batch(db_cursor, ('INSERT INTO cards_color_identity_staging'
    '(name, color) VALUES (%s, %s)'), list(cards_color_identity_args))
execute_batch(db_cursor, ('INSERT INTO cards_supertypes_staging'
    '(name, supertype) VALUES (%s, %s)'), list(cards_supertypes_args))
execute_batch(db_cursor, ('INSERT INTO cards_types_staging'
    '(name, type) VALUES (%s, %s)'), list(cards_types_args))
execute_batch(db_cursor, ('INSERT INTO cards_subtypes_staging'
    '(name, subtype) VALUES (%s, %s)'), list(cards_subtypes_args))
execute_batch(db_cursor, ('INSERT INTO cards_names_staging'
    '(name, alt_name) VALUES (%s, %s)'), list(cards_names_args))
execute_batch(db_cursor, ('INSERT INTO cards_variations_staging'
    '(name, id) VALUES (%s, %s)'), list(cards_variations_args))
execute_batch(db_cursor, ('INSERT INTO cards_rulings_staging'
    '(name, date, text) VALUES (%s, %s, %s)'), list(cards_rulings_args))
execute_batch(db_cursor, ('INSERT INTO cards_foreign_names_staging'
    '(name, text, flavor, image_url, language, multiverse_id) '
    'VALUES (%s, %s, %s, %s, %s, %s)'), list(cards_foreign_names_args))
execute_batch(db_cursor, ('INSERT INTO cards_printings_staging'
    '(name, set) VALUES (%s, %s)'), list(cards_printings_args))
execute_batch(db_cursor, ('INSERT INTO cards_legalities_staging'
    '(name, format, legality) VALUES (%s, %s, %s)'), list(cards_legalities_args))
if args.verbose:
    print(f'{len(cards_args)} rows inserted into cards table.')
    print(f'{len(cards_color_args)} rows inserted into colors table.')
    print(f'{len(cards_color_identity_args)} rows inserted into color '
          f'identity table.')
    print(f'{len(cards_supertypes_args)} rows inserted into supertypes '
          f'table.')
    print(f'{len(cards_types_args)} rows inserted into types table.')
    print(f'{len(cards_subtypes_args)} rows inserted into subtypes table.')
    print(f'{len(cards_names_args)} rows inserted into names table.')
    print(f'{len(cards_variations_args)} rows inserted into variations'
          f' table.')
    print(f'{len(cards_rulings_args)} rows inserted into rulings table.')
    print(f'{len(cards_foreign_names_args)} rows inserted into foreign names'
          f' table.')
    print(f'{len(cards_printings_args)} rows inserted into printings table.')
    print(f'{len(cards_legalities_args)} rows inserted into legalities '
          f'table.')

if args.verbose:
    print('Refreshing formats data staging table.')
formats = data['formats']
db_cursor.execute('DROP TABLE IF EXISTS formats_staging')
db_cursor.execute('CREATE TABLE formats_staging (name varchar(100))')
formats_args = list(map(lambda f: (f,), formats))
execute_batch(db_cursor, 'INSERT INTO formats_staging (name) VALUES (%s)',
              formats_args)
if args.verbose:
    print(f'{len(formats_args)} rows inserted.')

if args.verbose:
    print('Refreshing sets data staging table.')
sets = data['sets']
db_cursor.execute('DROP TABLE IF EXISTS sets_staging')
db_cursor.execute('''CREATE TABLE sets_staging (
    name varchar(100),
    block varchar(100),
    code varchar(20),
    gatherer_code varchar(20),
    old_code varchar(20),
    magic_cards_info_code varchar(20),
    release_date varchar(20),
    border varchar(50),
    expansion varchar(100),
    online_only boolean,
    booster jsonb)
    ''')
sets_args = list(map(lambda set: (
    set['name'],
    set['block'] if 'block' in set else '',
    set['code'] if 'code' in set else '',
    set['gatherer_code'] if 'gatherer_code' in set else '',
    set['old_code'] if 'old_code' in set else '',
    set['magic_cards_info_code'] if 'magic_cards_info_code' in set else '',
    set['release_date'] if 'release_date' in set else '',
    set['border'] if 'border' in set else '',
    set['expansion'] if 'expansion' in set else '',
    set['online_only'] if 'online_only' in set else False,
    json.dumps(set['booster']) if 'booster' in set else None
), sets))
execute_batch(db_cursor, ('INSERT INTO sets_staging (name, block, code,'
    'gatherer_code, old_code, magic_cards_info_code, release_date, border,'
    'expansion, online_only, booster) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '
    '%s, %s, %s)'), sets_args)
if args.verbose:
    print(f'{len(sets_args)} rows inserted.')

if args.verbose:
    print('Refreshing subtypes staging table.')
subtypes = data['subtypes']
db_cursor.execute('DROP TABLE IF EXISTS subtypes_staging')
db_cursor.execute('CREATE TABLE subtypes_staging (name varchar(50))')
subtypes_args = list(map(lambda st: (st,), subtypes))
execute_batch(db_cursor, 'INSERT INTO subtypes_staging (name) VALUES (%s)',
              subtypes_args)
if args.verbose:
    print(f'{len(subtypes_args)} rows inserted.')

if args.verbose:
    print('Refreshing supertypes staging table.')
supertypes = data['supertypes']
db_cursor.execute('DROP TABLE IF EXISTS supertypes_staging')
db_cursor.execute('CREATE TABLE supertypes_staging (name varchar(50))')
supertypes_args = list(map(lambda st: (st,), supertypes))
execute_batch(db_cursor, 'INSERT INTO supertypes_staging (name) VALUES (%s)',
              supertypes_args)
if args.verbose:
    print(f'{len(supertypes_args)} rows inserted.')

if args.verbose:
    print('Refreshing types staging table.')
types = data['types']
db_cursor.execute('DROP TABLE IF EXISTS types_staging')
db_cursor.execute('CREATE TABLE types_staging (name varchar(50))')
types_args = list(map(lambda t: (t,), types))
execute_batch(db_cursor, 'INSERT INTO types_staging (name) VALUES (%s)',
              types_args)
if args.verbose:
    print(f'{len(types_args)} rows inserted.')

db_conn.commit()
db_cursor.close()
db_conn.close()