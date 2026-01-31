def score_movie(movie, genre_weights):
    score = 0.0
    for g in movie.get("genre_ids", []):
        score += genre_weights.get(g, 0)

    score += movie.get("vote_average", 0) * 0.5
    score += movie.get("popularity", 0) * 0.01
    return score

def rank_movies(movies, genre_weights, seen_ids, limit=5):
    scored = []
    for m in movies:
        if m["id"] in seen_ids:
            continue
        scored.append((score_movie(m, genre_weights), m))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored[:limit]]
