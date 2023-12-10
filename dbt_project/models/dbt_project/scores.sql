SELECT
  "Date"::TIMESTAMP as "date",
  "rating"::INT,
  "user_id"::INT,
  "movie_id"::INT
FROM {{ source('raw_data', 'scores') }}
