SELECT
  "id"::INT,
  "occupation",
  "Active Since"::TIMESTAMP AS "active_since"
FROM {{ source('raw_data', 'users') }}
