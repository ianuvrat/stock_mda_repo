import sqlite3

# Connect to the database
conn = sqlite3.connect('results.db')
# Create a cursor object
cursor = conn.cursor()
# Select data from the table
cursor.execute("SELECT * FROM results")
# Fetch all the rows
rows = cursor.fetchall()

# Display the rows
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
