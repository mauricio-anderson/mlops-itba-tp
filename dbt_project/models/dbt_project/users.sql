SELECT
  "id"::INT,
  "occupation",
  "Active Since"::TIMESTAMP AS "active_since"
FROM "raw_data"."users"