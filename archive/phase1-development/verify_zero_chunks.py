import psycopg2

conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/researchnexus")
cur = conn.cursor()

# 1. Does 2504.02249v2 have chunks?
cur.execute("SELECT COUNT(*) FROM paper_chunks WHERE paper_id='2504.02249v2'")
chunk_count = cur.fetchone()[0]

# 2. Does 2504.02249v2 exist in papers?
cur.execute("SELECT title, read_source FROM papers WHERE id='2504.02249v2'")
row = cur.fetchone()

print(f"Paper 2504.02249v2:")
print(f"Title: {row[0] if row else 'NOT FOUND'}")
print(f"Chunks in PG: {chunk_count}")
print(f"Read Source: {row[1] if row else 'N/A'}")

cur.close()
conn.close()
