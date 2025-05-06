import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('journal.db')
cursor = conn.cursor()

from datetime import datetime

# Ensure the entries table exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
)
''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES entries (id)
)
''')
conn.commit()

def add_entry(content):
    created_at = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('INSERT INTO entries (content, created_at) VALUES (?, ?)', (content, created_at))
    conn.commit()

def view_entries(date_filter=None):
    if date_filter:
        cursor.execute('SELECT * FROM entries WHERE created_at = ?', (date_filter,))
    else:
        cursor.execute('SELECT * FROM entries')
    return cursor.fetchall()

def update_entry(entry_id, new_content):
    updated_at = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('UPDATE entries SET content = ?, created_at = ? WHERE id = ?',
                   (new_content, updated_at, entry_id))
    conn.commit()

def delete_entry(entry_id):
    cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id))
    conn.commit()
    
def search_entries(keyword):
    cursor.execute('SELECT * FROM entries WHERE content LIKE ?', ('%' + keyword + '%',))
    return cursor.fetchall()

def filter_entries_by_date_range(start_date, end_date):
    cursor.execute('SELECT * FROM entries WHERE created_at BETWEEN ? AND ?', (start_date, end_date))
    return cursor.fetchall()

def add_tag(entry_id, tag):
    cursor.execute('INSERT INTO tags (entry_id, tag) VALUES (?, ?)', (entry_id, tag))
    conn.commit()

def get_entries_by_tag(tag):
    cursor.execute('''
    SELECT entries.id, entries.content, entries.created_at
    FROM entries
    JOIN tags ON entries.id = tags.entry_id
    WHERE tags.tag = ?
    ''', (tag,))
    return cursor.fetchall()