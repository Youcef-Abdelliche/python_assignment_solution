import xml.etree.ElementTree as et
import _sqlite3

conn = _sqlite3.connect("tracksdb.sqlite")
cur = conn.cursor()


#cur.execute('DELETE FROM Artist')
#cur.execute('DELETE FROM Genre')
#cur.execute('DELETE FROM Album')
#cur.execute('DELETE FROM Track')

cur.execute('DROP TABLE IF EXISTS Artist')
#cur.execute('DELETE FROM Artist')

cur.execute(' DROP TABLE IF EXISTS Genre')
#cur.execute('DELETE FROM Genre')

cur.execute(' DROP TABLE IF EXISTS Album')
#cur.execute('DELETE * FROM Album')

cur.execute(' DROP TABLE IF EXISTS Track')
#cur.execute('DELETE * FROM Track')

cur.execute('''
    CREATE TABLE Artist (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE
    )''')
cur.execute('''
    CREATE TABLE Genre (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE
    )''')

cur.execute('''
    CREATE TABLE Album (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        artist_id  INTEGER,
        title   TEXT UNIQUE
    )''')
cur.execute('''CREATE TABLE Track (
        id  INTEGER NOT NULL PRIMARY KEY 
            AUTOINCREMENT UNIQUE,
        title TEXT  UNIQUE,
        album_id  INTEGER,
        genre_id  INTEGER,
        len INTEGER, rating INTEGER, count INTEGER
    )''')

file = open("Library.xml")
stuff = et.parse(file)
all_data = stuff.findall('dict/dict/dict')


def lookup(d, key):
    found = False
    for child in d:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


for data in all_data:
    if lookup(data, 'Track ID') is None:
        continue

    name = lookup(data, 'Name')
    artist = lookup(data, 'Artist')
    album = lookup(data, 'Album')
    genre = lookup(data, 'Genre')
    count = lookup(data, 'Play Count')
    rating = lookup(data, 'Rating')
    length = lookup(data, 'Total Time')

    if name is None or artist is None or album is None or genre is None:
        continue
    cur.execute('''
    INSERT OR IGNORE INTO Artist(name) VALUES (?)''', (artist,))
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = cur.fetchone()[0]

    cur.execute('''
        INSERT OR IGNORE INTO Genre(name) VALUES (?)''', (genre,))
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = cur.fetchone()[0]

    cur.execute('''
            INSERT OR IGNORE INTO Album(title, artist_id) VALUES (?, ?)''', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = cur.fetchone()[0]

    cur.execute('''
            INSERT OR REPLACE INTO Track(title, album_id, genre_id, len, rating, count)
            VALUES (?, ?, ?, ?, ?, ?)''', (name, album_id, genre_id, length, rating, count))

conn.commit()

query = '''
SELECT Track.title, Artist.name, Album.title, Genre.name 
    FROM Track JOIN Genre JOIN Album JOIN Artist 
    ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
        AND Album.artist_id = Artist.id
    ORDER BY Artist.name LIMIT 3'''

for row in cur.execute(query):
    print(str(row[0]), str(row[1]), str(row[2]), str(row[3]))

conn.close()
