import sqlite3

def store_result(page_number, type, result):
    conn = sqlite3.connect('results.db')
    conn.execute("INSERT INTO results (page_number, type, result) VALUES (?, ?, ?)", (page_number, type, result))
    conn.commit()
    conn.close()





