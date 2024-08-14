CREATE TABLE IF NOT EXISTS music (
	user_id	BIGINT,
	url	TEXT,
	service	TEXT
);
CREATE TABLE IF NOT EXISTS watched_videos (
	user_id	BIGINT,
	url	TEXT,
	service	TEXT
);
CREATE TABLE IF NOT EXISTS to_watch (
	user_id	BIGINT,
	url	TEXT,
	service	TEXT
);

CREATE TABLE IF NOT EXISTS MISC_VIDEOS (
	user_id	BIGINT,
	url	TEXT,
	service	TEXT
);

CREATE TABLE IF NOT EXISTS tech_videos (
	user_id	BIGINT,
	url	TEXT,
	service	TEXT
);

CREATE TABLE IF NOT EXISTS anime_videos (
	user_id	BIGINT,
	url	TEXT,
	service	TEXT
);

CREATE TABLE CONTENT(
  user_id BIGINT NOT NULL,
  url TEXT NOT NULL,
  service TEXT,
  content_type smallint,
  PRIMARY KEY(url, service, content_type)
);