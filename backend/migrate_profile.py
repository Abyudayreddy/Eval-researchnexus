import psycopg2
import os
from dotenv import load_dotenv

def run_migration():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not found in .env")
        return

    # Extract connection args from postgresql://postgres:password@localhost:5432/researchnexus
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Add new profile columns
        columns_to_add = [
            "title VARCHAR",
            "institution VARCHAR",
            "bio TEXT",
            "location VARCHAR",
            "website VARCHAR",
            "orcid VARCHAR",
            "google_scholar VARCHAR"
        ]
        
        for col in columns_to_add:
            col_name = col.split(" ")[0]
            print(f"Adding column {col_name} to users table...")
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col};")
                conn.commit()
                print(f"✅ Success")
            except psycopg2.errors.DuplicateColumn:
                print(f"⚠️ Column {col_name} already exists. Skipping.")
                conn.rollback()
            except Exception as e:
                print(f"❌ Error adding {col_name}: {e}")
                conn.rollback()

        cur.close()
        conn.close()
        print("\nMigration completed successfully!")
        
    except Exception as e:
        print(f"Failed to connect to database: {e}")

if __name__ == "__main__":
    run_migration()
