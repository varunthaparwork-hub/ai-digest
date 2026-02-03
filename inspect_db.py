import sqlite3

conn = sqlite3.connect("data/digest.db")
cur = conn.cursor()

print("TABLES:")
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cur.fetchall())

print("\nEVALUATIONS SCHEMA:")
cur.execute("PRAGMA table_info(evaluations)")
for row in cur.fetchall():
    print(row)

conn.close()
