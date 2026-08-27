import sqlite3, os
db_path = os.path.join('backend', 'wariseva.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT * FROM pilgrims WHERE wari_id='WS-28471'")
row = c.fetchone()
if row:
    print(dict(row))
else:
    print("Not found in pilgrims, checking fallback in app.py")
