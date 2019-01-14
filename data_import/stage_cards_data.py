import psycopg2
import argparse
import json
from collections import deque
from psycopg2.extras import execute_batch

parser = argparse.ArgumentParser()
parser.add_argument('file', help='Path to file containing cards data.',
                    type=str)
parser.add_argument('--verbose', help='Print progress messages.',
                    action='store_true')
args = parser.parse_args()
DB_CONN_STRING = 'dbname=cardconf'

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
db_cursor.execute('''CREATE TABLE cards_color_staging (
    name character varying(400),
    color character varying(20)
    )''')
db_cursor.execute('DROP TABLE IF EXISTS cards_color_identity_staging')
db_cursor.execute('''CREATE TABLE cards_color_identity_staging (
    name character varying(400),
    color character varying(20)
    )''')

card_rows_counter = 0
cards = data['cards']
cards_staging_args = [None for _ in range(len(cards))]
color_staging_args = deque()
color_identity_staging_args = deque()
for card_index in range(len(cards)):
    name_arg = cards[card_index]['name']
    layout_arg = cards[card_index]['layout'] if 'layout' in \
        cards[card_index] else ''
    cmc_arg = cards[card_index]['cmc'] if 'cmc' in \
        cards[card_index] else None
    type_arg = cards[card_index]['type'] if 'type' in \
        cards[card_index] else ''
    supertypes_arg = json.dumps(cards[card_index]['supertypes']) if \
        'supertypes' in cards[card_index] else None
    types_arg = json.dumps(cards[card_index]['types']) if \
        'types' in cards[card_index] else None
    subtypes_arg = json.dumps(cards[card_index]['subtypes']) if \
        'subtypes' in cards[card_index] else None
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
    names_arg = json.dumps(cards[card_index]['names']) if 'names' in \
        cards[card_index] else None
    mana_cost_arg = cards[card_index]['manaCost'] if 'manaCost' in \
        cards[card_index] else ''
    variations_arg = json.dumps(cards[card_index]['variations']) if \
        'variations' in cards[card_index] else None
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
    rulings_arg = json.dumps(cards[card_index]['rulings']) if \
        'rulings' in cards[card_index] else None
    foreign_names_arg = \
        json.dumps(cards[card_index]['foreignNames']) if \
        'foreignNames' in cards[card_index] else None
    printings_arg = json.dumps(cards[card_index]['printings']) if \
        'printings' in cards[card_index] else None
    original_text_arg = cards[card_index]['originalText'] if \
        'originalText' in cards[card_index] else ''
    original_type_arg = cards[card_index]['originalType'] if \
        'originalType' in cards[card_index] else ''
    legalities_arg = json.dumps(cards[card_index]['legalities']) if \
        'legalities' in cards[card_index] else None
    source_arg = cards[card_index]['source'] if 'source' in \
        cards[card_index] else ''
    multiverse_id_arg = cards[card_index]['multiverseId'] if \
        'multiverseId' in cards[card_index] else None
    cards_staging_args[card_index] = (name_arg, layout_arg, cmc_arg,
        type_arg, supertypes_arg, types_arg, subtypes_arg, rarity_arg,
        set_arg, set_name_arg, text_arg, flavor_arg, artist_arg,
        number_arg, power_arg, toughness_arg, loyalty_arg, names_arg,
        power_arg, toughness_arg, loyalty_arg, names_arg, mana_cost_arg,
        variations_arg, image_url_arg, watermark_arg, border_arg,
        timeshifted_arg, hand_arg, life_arg, reserved_arg,
        release_date_arg, starter_arg, rulings_arg, foreign_names_arg,
        printings_arg, original_text_arg, original_type_arg,
        legalities_arg, source_arg, multiverse_id_arg)
    # Name does not uniquely identify a card, but that is ok for the
    # purposes of the staging table. The query the accesses the color
    # staging tables should be written to distinctly select color data.
    if 'colors' in cards[card_index]:
        for color in cards[card_index]['colors']:
            color_staging_args.append((name_arg, color))
    if 'colorIdentity' in cards[card_index]:
        for color in cards[card_index]['colorIdentity']:
            color_identity_staging_args.append((name_arg, color))
    if args.verbose:
        card_rows_counter += len(cards_staging_args)
        card_rows_counter += len(color_staging_args)
        card_rows_counter += len(color_identity_staging_args)
    execute_batch(db_cursor, ('INSERT INTO cards_staging (name, layout,'
        'cmc, type, supertypes, types, subtypes, rarity, set, set_name, text,'
        'flavor, artist, number, power, toughness, loyalty, names, mana_cost,'
        'variations, image_url, watermark, border, timeshifted, hand, life,'
        'reserved, release_date, starter, rulings, foreign_names, printings,'
        'original_text, original_type, legalities, source, multiverse_id)'
        'VALUES (%, %, %, %, %, %, %, %, %, %, %, %, %, %, %, %, %, %, %, %,'
        '%, %, %, %, %, %, %, %, %, %, %, %, %, %, %, %, %)'),
        cards_staging_args)
    execute_batch(db_cursor, ('INSERT INTO cards_color_staging (name,'
        'color) VALUES (%, %)'),list(color_staging_args))
    execute_batch(db_cursor, ('INSERT INTO cards_color_identity_staging '
        '(name, color) VALUES (%, %)'), list(color_identity_staging_args))
if args.verbose:
    print(f'{card_rows_counter} rows inserted.')

if args.verbose:
    print('Refreshing formats data staging table.')
db_cursor.execute('DROP TABLE IF EXISTS formats_staging')
db_cursor.execute('CREATE TABLE formats_staging (name varchar(100))')
formats_staging_args = list(map(lambda f: (f,), formats))
execute_batch(db_cursor, 'INSERT INTO formats_staging (name) VALUES (%)',
              formats_staging_args)
if args.verbose:
    print(f'{len(formats_staging_args)} rows inserted.')

if args.verbose:
    print('Refreshing sets data staging table.')
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
sets_staging_args = list(map(lambda set: (
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
db_cursor.execute(('INSERT INTO sets_staging (name, block, code,'
    'gatherer_code, old_code, magic_cards_info_code, release_date, border,'
    'expansion, online_only, booster) VALUES (%, %, %, %, %, %, %, %, %, %,'
    '%)'), sets_staging_args)
if args.verbose:
    print(f'{len(sets_staging_args)} rows inserted.')

if args.verbose:
    print('Refreshing subtypes staging table.')
db_cursor.execute('DROP TABLE IF EXISTS subtypes_staging')
db_cursor.execute('CREATE TABLE subtypes_staging (name varchar(50))')
subtypes_staging_args = list(map(lambda st: (st,), subtypes))
execute_batch(db_cursor, 'INSERT INTO subtypes_staging (name) VALUES (%)',
              subtypes_staging_args)
if args.verbose:
    print(f'{len(subtypes_staging_args)} rows inserted.')

if args.verbose:
    print('Refreshing supertypes staging table.')
db_cursor.execute('DROP TABLE IF EXISTS supertypes_staging')
db_cursor.execute('CREATE TABLE supertypes_staging (name varchar(50))')
supertypes_staging_args = list(map(lambda st: (st,), supertypes))
execute_batch(db_cursor, 'INSERT INTO supertypes_staging (name) VALUES (%)',
              supertypes_staging_args)
if args.verbose:
    print(f'{len(subtypes_staging_args)} rows inserted.')

if args.verbose:
    print('Refreshing types staging table.')
db_cursor.execute('DROP TABLE IF EXISTS types_staging')
db_cursor.execute('CREATE TABLE types_staging (name varchar(50))')
types_staging_args = list(map(lambda t: (t,), types))
execute_batch(db_cursor, 'INSERT INTO types_staging (name) VALUES (%)',
              types_staging_args)
if args.verbose:
    print(f'{len(types_staging_args)} rows inserted.')