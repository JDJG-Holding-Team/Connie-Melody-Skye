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

CREATE TABLE IF NOT EXISTS idk_videos (
	user_id	BIGINT,
	url	TEXT,
	service	TEXT
);

CREATE TABLE IF NOT EXISTS tech_videos (
	user_id	BIGINT,
	url	TEXT,
	service	TEXT
);
