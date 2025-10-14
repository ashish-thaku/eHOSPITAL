import sqlite3
import os

DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')

if not os.path.exists(DB):
    print('No db.sqlite3 found at', DB)
    raise SystemExit(1)

conn = sqlite3.connect(DB)
cur = conn.cursor()

try:
    cur.execute("SELECT id, username, email, is_staff, is_superuser FROM auth_user WHERE is_superuser=1")
    rows = cur.fetchall()
    if not rows:
        print('No superuser rows found in auth_user')
    else:
        print('Superuser accounts found:')
        for r in rows:
            print(f"id: {r[0]}, username: {r[1]}, email: {r[2]}, is_staff: {r[3]}, is_superuser: {r[4]}")
except Exception as e:
    print('Error querying auth_user:', e)
finally:
    conn.close()
