import duckdb

# Connect to a database (creates a file if it doesn't exist)
conn = duckdb.connect("my_database.duckdb")

# Create a table
conn.execute("""
    CREATE TABLE users (
        id INTEGER,
        name TEXT,
        age INTEGER,
        city TEXT
    )
""")

# Insert some data
conn.execute("INSERT INTO users VALUES (1, 'John', 25, 'New York')")
conn.execute("INSERT INTO users VALUES (2, 'Alice', 30, 'San Diego')")

# Query the data
result = conn.execute("SELECT * FROM users").fetchall()

# Print results
print(result)

# Close the connection
conn.close()