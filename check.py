import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

result = cursor.execute("SELECT url from watched_videos")
urls = result.fetchall()

print(list(urls))

# could use a little bit more than this.

connection.close()
