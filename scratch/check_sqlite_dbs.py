import os
import sqlite3

dbs = ['papers.db', 'researchnexus_eval.db', 'test.db']
for d in dbs:
    if os.path.exists(d):
        conn = sqlite3.connect(d)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        t = [x[0] for x in c.fetchall()]
        print(f"DB {d}: {len(t)} tables -> {t}")
        for tbl in t[:5]:
            c.execute(f"SELECT count(*) FROM {tbl}")
            cnt = c.fetchone()[0]
            print(f"   {tbl}: {cnt} rows")
        conn.close()
    else:
        print(f"DB {d}: not found")
