import json
import _sqlite3

conn = _sqlite3.connect("coursesdb.sqlite")
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)''')

data = open("roster_data.json").read()
js = json.loads(data)

for entry in js:
    user = entry[0]
    course = entry[1]
    role = entry[2]

    cur.execute('INSERT OR IGNORE INTO User(name) VALUES (?)', (user,))
    cur.execute('SELECT id FROM User WHERE name = ?', (user,))
    user_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course(title) VALUES (?)', (course,))
    cur.execute('SELECT id FROM Course WHERE title = ?', (course,))
    course_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Member(user_id, course_id, role) VALUES (?, ?, ?)', (user_id, course_id, role))

conn.commit()

query = '''
    SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X'''

for row in cur.execute(query):
    print(row[0])
