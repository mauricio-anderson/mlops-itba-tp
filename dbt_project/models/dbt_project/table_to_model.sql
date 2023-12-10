SELECT
    -- SCORES
   "user_id", "movie_id",  "date", "rating",
    -- USERS
    "occupation", "active_since"
    -- MOVIES
    "name", "release_date", "imdb_url", "war", "crime",
    "drama", "action", "comedy", "horror", "sci_fi", "fantasy",
    "musical", "mystery", "romance", "western", "unknown",
    "thriller", "adventure", "animation", "film_noir", "childrens", "documentary"
FROM {{ ref('scores') }} a
  LEFT JOIN {{ ref('users') }} b ON a.user_id=b.id
  LEFT JOIN {{ ref('movies') }} c ON a.movie_id=c.id
