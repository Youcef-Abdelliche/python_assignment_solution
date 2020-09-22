import _sqlite3

conn = _sqlite3.connect("orgdb.sqlite")
cur = conn.cursor()

try:
    cur.execute('DROP TABLE IF EXISTS Counts')
    cur.execute('DELETE FROM Counts')
except:
    cur.execute('''
        CREATE TABLE Counts (org TEXT, count INTEGER)''')
file = open("text.txt")

for line in file:
    if not line.startswith("From "):
        continue
    line = line.strip()
    lst = line.split()
    lst = lst[1].split('@')
    org = lst[1]
    cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts(org, count) VALUES (?, 1)', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count +1 WHERE org = ?', (org,))
conn.commit()

query = 'SELECT org FROM Counts WHERE count = 536'
for row in cur.execute(query):
    print(str(row[0]))
