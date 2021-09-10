/*

===================================================
Creates WOE table for location data.
===================================================

Created by: Mitchell Bregman

*/

CREATE OR REPLACE TABLE viral_t.woe (
  woe_id        NUMBER        NOT NULL,
  name          VARCHAR(100)  NOT NULL,
  latitude      FLOAT,
  longitude     FLOAT,
  PRIMARY KEY (woe_id)
);

INSERT INTO viral_t.woe (woe_id, name, latitude, longitude)
VALUES  (1, 'global', NULL, NULL),
        (23424977, 'usa', NULL, NULL),
        (2459115, 'usa-nyc', 40.712776, -74.005974),
        (2442047, 'usa-lax', 34.052235, -118.243683),
        (2379574, 'usa-chi', 41.878113, -87.629799),
        (2388929, 'usa-dal', 32.776665, -96.796989),
        (2424766, 'usa-hou', 29.760427, -95.369804),
        (2514815, 'usa-wdc', 38.89499, -77.03656),
        (2450022, 'usa-mia', 25.77417, -80.19362),
        (2471217, 'usa-phi', 39.95272, -75.16353),
        (2357024, 'usa-atl', 33.74899, -84.39026),
        (2367105, 'usa-bos', 42.36025, -71.05829),
        (2471390, 'usa-phx', 33.44844, -112.07414),
        (2487956, 'usa-sfo', 37.77903, -122.41991),
        (2391585, 'usa-det', 42.33155, -83.04664),
        (2490383, 'usa-sea', 47.60383, -122.33006)
