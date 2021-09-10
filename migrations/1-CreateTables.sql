/*

===================================================
Creates schema and tables required for import data.
===================================================

Created by: Leon Kozlowski
Modified by:
- Mitchell Bregman

*/

CREATE SCHEMA IF NOT EXISTS viral_t;

CREATE OR REPLACE TABLE viral_t.trends (
  id            NUMBER        AUTOINCREMENT,
  date_created  DATETIME      NOT NULL,
  metro         VARCHAR(10)   NOT NULL,
  woe           NUMBER        NOT NULL,
  name          VARCHAR(100)  NOT NULL,
  url           VARCHAR(250)  NOT NULL,
  promoted      VARCHAR(100)  DEFAULT NULL,
  querystring   VARCHAR(100)  NOT NULL,
  volume        NUMBER,
  PRIMARY KEY (id)
);

CREATE OR REPLACE TABLE viral_t.tweets (
  id                NUMBER        AUTOINCREMENT,
  date_created      DATETIME      NOT NULL,
  tweet_created_at  DATETIME      NOT NULL,
  tweet_id          NUMBER        NOT NULL,
  text              VARCHAR(140)  NOT NULL,
  username          VARCHAR(60)   NOT NULL,
  verified          BOOLEAN,
  lang              VARCHAR(10),
  truncated         BOOLEAN       DEFAULT NULL,
  favorites         NUMBER,
  retweets          NUMBER,
  trend             VARCHAR(100)  NOT NULL,
  PRIMARY KEY (id)
);

CREATE OR REPLACE TABLE viral_t.images (
  id            NUMBER    AUTOINCREMENT,
  date_created  DATETIME  NOT NULL,
  tweets_id     NUMBER,
  url           VARCHAR(100),
  PRIMARY KEY (id)
);