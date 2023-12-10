SELECT
  "id"::INT,
  "Name" AS "name",
  "Release Date"::TIMESTAMP AS "release_date",
  "IMDB URL" AS "imdb_url",
  "war"::INT::BOOLEAN,
  "crime"::INT::BOOLEAN,
  "drama"::INT::BOOLEAN,
  "Action"::INT::BOOLEAN AS "action",
  "comedy"::INT::BOOLEAN,
  "horror"::INT::BOOLEAN,
  "Sci-Fi" AS "sci_fi",
  "fantasy"::INT::BOOLEAN,
  "musical"::INT::BOOLEAN,
  "mystery"::INT::BOOLEAN,
  "romance"::INT::BOOLEAN,
  "western"::INT::BOOLEAN,
  "unknown"::INT::BOOLEAN,
  "thriller"::INT::BOOLEAN,
  "adventure"::INT::BOOLEAN,
  "animation"::INT::BOOLEAN,
  "Film-Noir"::INT::BOOLEAN AS "film_noir",
  "Children's"::INT::BOOLEAN AS "childrens",
  "documentary"::INT::BOOLEAN
FROM "raw_data"."movies"