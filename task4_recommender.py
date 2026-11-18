"""CodSoft AI Internship - Task 4: Movie Recommendation System
Two techniques, pure Python (no installs needed):
 1) Content-based filtering  - cosine similarity on genre vectors
 2) Collaborative filtering  - user-based, cosine similarity on ratings
Then a hybrid score that blends both."""
import math
from collections import defaultdict

MOVIES = {
    "Inception":        ["sci-fi", "thriller", "action"],
    "Interstellar":     ["sci-fi", "drama", "adventure"],
    "The Matrix":       ["sci-fi", "action"],
    "The Dark Knight":  ["action", "crime", "thriller"],
    "Titanic":          ["romance", "drama"],
    "The Notebook":     ["romance", "drama"],
    "Toy Story":        ["animation", "comedy", "family"],
    "Finding Nemo":     ["animation", "family", "adventure"],
    "The Hangover":     ["comedy"],
    "Superbad":         ["comedy"],
    "Se7en":            ["crime", "thriller", "drama"],
    "Avengers: Endgame":["action", "sci-fi", "adventure"],
    "La La Land":       ["romance", "drama", "musical"],
    "Coco":             ["animation", "family", "musical"],
    "Zindagi Na Milegi Dobara": ["comedy", "drama", "adventure"],
}

RATINGS = {  # user -> {movie: rating 1-5}
    "Aman":   {"Inception": 5, "The Matrix": 5, "The Dark Knight": 4, "Titanic": 2, "Se7en": 4},
    "Bhavna": {"Titanic": 5, "The Notebook": 5, "La La Land": 4, "Toy Story": 3, "Coco": 4},
    "Chetan": {"Toy Story": 5, "Finding Nemo": 5, "Coco": 5, "The Hangover": 3},
    "Divya":  {"Inception": 4, "Interstellar": 5, "Avengers: Endgame": 4, "The Matrix": 4},
    "Esha":   {"The Hangover": 5, "Superbad": 5, "Zindagi Na Milegi Dobara": 4, "Toy Story": 3},
}


def cosine(a, b):
    keys = set(a) & set(b)
    num = sum(a[k] * b[k] for k in keys)
    den = math.sqrt(sum(v*v for v in a.values())) * math.sqrt(sum(v*v for v in b.values()))
    return num / den if den else 0.0


# ---------- content-based ----------
GENRE_VEC = {m: {g: 1 for g in gs} for m, gs in MOVIES.items()}


def content_scores(user_ratings):
    scores = defaultdict(float)
    for liked, r in user_ratings.items():
        if r < 4:
            continue
        for m in MOVIES:
            if m not in user_ratings:
                scores[m] += r * cosine(GENRE_VEC[liked], GENRE_VEC[m])
    return scores


# ---------- collaborative ----------
def collab_scores(user):
    me = RATINGS[user]
    scores, norm = defaultdict(float), defaultdict(float)
    for other, theirs in RATINGS.items():
        if other == user:
            continue
        sim = cosine(me, theirs)
        for m, r in theirs.items():
            if m not in me:
                scores[m] += sim * r
                norm[m] += abs(sim)
    return {m: scores[m] / norm[m] for m in scores if norm[m]}


def recommend(user, n=5, mode="hybrid"):
    me = RATINGS[user]
    cb = content_scores(me)
    cf = collab_scores(user)
    top = lambda d: max(d.values(), default=1) or 1
    cbn, cfn = top(cb), top(cf)
    final = {}
    for m in MOVIES:
        if m in me:
            continue
        c1, c2 = cb.get(m, 0) / cbn, cf.get(m, 0) / cfn
        final[m] = {"content": c1, "collab": c2, "hybrid": 0.5*c1 + 0.5*c2}[mode]
    return sorted(final.items(), key=lambda x: -x[1])[:n]


if __name__ == "__main__":
    print("Users:", ", ".join(RATINGS))
    name = input("Enter a user name (default Aman): ").strip().title() or "Aman"
    if name not in RATINGS:
        print("Unknown user, using Aman.")
        name = "Aman"
    print(f"\nMovies {name} rated: {RATINGS[name]}\n")
    for mode in ("content", "collab", "hybrid"):
        print(f"--- {mode.upper()} recommendations for {name} ---")
        for i, (m, s) in enumerate(recommend(name, 3, mode), 1):
            print(f"{i}. {m}  (score {s:.2f})")
        print()
