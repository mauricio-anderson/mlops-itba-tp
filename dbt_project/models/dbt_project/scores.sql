SELECT
  "Date"::TIMESTAMP as "date",
  "rating"::INT,
  "user_id"::INT,
  "movie_id"::INT
FROM "raw_data"."scores"