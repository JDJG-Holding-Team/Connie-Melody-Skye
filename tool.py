import json
import sqlite3

with open('data.json') as json_file:
    data = json.load(json_file)

urls = [(168422909482762240, item, "YouTube") for item in data["messages"]]

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.executemany('INSERT INTO watched_videos (user_id, url, service) VALUES (?, ?, ?)', urls)

connection.commit()
connection.close()

result = cursor.execute("SELECT url from watched_videos")
urls = result.fetchall()

print(dict(urls))