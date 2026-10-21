import psycopg2

def main():
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/researchnexus")
    cur = conn.cursor()
    cur.execute("SELECT id, title, authors, domain_id, abstract FROM papers LIMIT 5")
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Title: {row[1]}")
        print(f"Authors: {row[2]}")
        print(f"Domain: {row[3]}")
        print(f"Abstract: {row[4][:100]}...")
        print()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
