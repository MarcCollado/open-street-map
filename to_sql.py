import sqlite3
import csv
from pprint import pprint

sqlite_file = 'osm.db'
conn = sqlite3.connect(sqlite_file)

cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS node, node_tags, way, way_nodes, way_tags;')
# conn.commit()

cur.execute('''
    CREATE TABLE node (
        id INTEGER PRIMARY KEY,
        lat REAL,
        lon REAL,
        user TEXT,
        uid INTEGER,
        version TEXT,
        changeset INTEGER,
        timestamp TEXT
        );
        ''')

conn.commit()

with open('output/node.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'], i['lat'], i['lon'], i['user'].decode('utf-8'), i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany('INSERT INTO node(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', to_db)

conn.commit()


cur.execute('''
    CREATE TABLE node_tags (
        id INTEGER REFERENCES node (id),
        key TEXT,
        value TEXT,
        type TEXT
        );
        ''')

conn.commit()

with open('output/node_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'], i['key'], i['value'].decode('utf-8'), i['type']) for i in dr]
cur.executemany('INSERT INTO node_tags(id, key, value, type) VALUES (?, ?, ?, ?);', to_db)

conn.commit()


cur.execute('''
    CREATE TABLE way (
        id INTEGER PRIMARY KEY,
        user TEXT,
        uid INTEGER,
        version TEXT,
        changeset INTEGER,
        timestamp TEXT
        );
        ''')

conn.commit()

with open('output/way.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'], i['user'].decode('utf-8'), i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany('INSERT INTO way(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);', to_db)

conn.commit()


cur.execute('''
    CREATE TABLE way_nodes (
        id INTEGER REFERENCES way (id),
        node_id INTEGER,
        position INTEGER
        );
        ''')

conn.commit()

with open('output/way_nodes.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]
cur.executemany('INSERT INTO way_nodes(id, node_id, position) VALUES (?, ?, ?);', to_db)

conn.commit()


cur.execute('''
    CREATE TABLE way_tags (
        id INTEGER REFERENCES way (id),
        key TEXT,
        value TEXT,
        type TEXT
        );
        ''')

conn.commit()

with open('output/way_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'], i['key'], i['value'].decode('utf-8'), i['type']) for i in dr]
cur.executemany('INSERT INTO way_tags(id, key, value, type) VALUES (?, ?, ?, ?);', to_db)

conn.commit()


cur.execute('SELECT * FROM node_tags')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)

conn.close()
