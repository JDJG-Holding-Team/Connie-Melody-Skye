CREATE TABLE CONTENT(
  user_id BIGINT NOT NULL,
  url TEXT NOT NULL,
  service TEXT,
  content_type smallint,
  PRIMARY KEY(url, service, content_type)
);
