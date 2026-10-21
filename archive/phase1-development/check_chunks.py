import psycopg2

conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/researchnexus")
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM paper_chunks WHERE paper_id='2504.02249v2'")
print('Chunks:', cur.fetchone()[0])
