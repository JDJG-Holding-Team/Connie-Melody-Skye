# MusicFinder
This Bot is designed to help find music using the database


If you want to your own values to the database you can try:

```postgresql
INSERT INTO data VALUES (user_id, url, service)
```

For Example:

```postgresql
INSERT INTO data VALUES (168422909482762240, 'https://youtu.be/arT86rIFM7k?si=Cg-KSSz5qU18wPH3', 'YouTube')
```

Please note that table.sql and exported.sql are designed to work with postgresql right now, if you want to use the data not in the bot with asqlite go ahead(it's still here as a requirements.txt)
