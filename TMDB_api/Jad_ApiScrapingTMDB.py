#!/usr/bin/env python3
"""
simple tmdb scraper that collects a target number of unique movies.
"""

import requests
import csv
import time
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# === configuration ===
target = 1000                 # how many unique movies to collect (change if needed)
save_every = 100              # save intermediate csv every N movies
sleep_between_requests = 0.25 # polite delay between requests to avoid rate limits
discover_sort = "popularity.desc"
comedy_genre_id = 35         # genre filter (35 = comedy). remove or change if you want
# max_discover_pages = 1000    # I changed this to 2 for testing how much time it takes
max_discover_pages = 2     # max pages to iterate (tmdb may allow high values)
# output_csv = "tmdb_movies_target_count.csv"
output_csv = "test.csv"
request_timeout = 15
max_retries = 3

# fields for the output csv
FIELDNAMES = [
    "tmdb_id", "title", "release_date", "year", "original_language", "runtime",
    "genres", "budget", "revenue", "popularity", "vote_average", "vote_count",
    "director", "top_actors", "overview", "success_label", "success_reason"
]

# === helpers ===
def tmdb_get(path, params=None):
    # simple wrapper for tmdb get with retries
    if params is None:
        params = {}
    params.update({"api_key": API_KEY, "language": "en-US"})
    url = f"{BASE_URL}{path}"
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(url, params=params, timeout=request_timeout)
            if r.status_code == 200:
                return r.json()
            else:
                print(f"[warn] {r.status_code} for {url} (attempt {attempt}) -> {r.text[:200]}")
        except Exception as e:
            print(f"[error] request exception for {url} (attempt {attempt}): {e}")
        # simple backoff
        time.sleep(1 * attempt)
    return None

def discover_movies_by_genre(genre_id, page=1):
    # discover movies filtered by genre (returns json or {})
    params = {
        "with_genres": genre_id,
        "sort_by": discover_sort,
        "page": page,
    }
    return tmdb_get("/discover/movie", params) or {}

def fetch_movie_details(movie_id):
    # movie details endpoint
    return tmdb_get(f"/movie/{movie_id}")

def fetch_movie_credits(movie_id):
    # credits endpoint to get cast & crew
    return tmdb_get(f"/movie/{movie_id}/credits")

def top_actors_from_credits(credits, n=3):
    # read top n actors from credits (order is usually meaningful)
    if not credits:
        return []
    cast = credits.get("cast", [])
    return [c.get("name") for c in cast[:n] if c.get("name")]

def director_from_credits(credits):
    # find director name in crew
    if not credits:
        return ""
    for c in credits.get("crew", []):
        if c.get("job") == "Director":
            return c.get("name", "")
    return ""

def classify_success(budget, revenue, vote_average, vote_count):
    # simple heuristic to decide if movie was successful
    # if budget/revenue missing, judge by votes/score only
    if not budget or not revenue or budget <= 0:
        if vote_average and vote_count and vote_average >= 7 and vote_count >= 500:
            return "critically good", "high user score & significant votes (no financials)"
        if vote_average and vote_average >= 6:
            return "average/positive", "decent user score (no financials)"
        return "unknown", "insufficient financial data"
    # with financials:
    if revenue >= 2 * budget and vote_average and vote_average >= 7 and vote_count >= 2000:
        return "blockbuster", f"revenue >= 2x budget ({revenue} >= {2*budget}), strong ratings"
    if revenue >= 1.2 * budget and vote_average and vote_average >= 6 and vote_count >= 500:
        return "hit", "revenue >= 1.2x budget and decent ratings"
    if revenue >= budget or (vote_average and vote_average >= 6):
        return "moderate", "at least broke even or decent ratings"
    return "flop", "revenue < budget and low ratings"

def save_movies_to_csv(movies, filename=output_csv):
    # write movies list of dicts to csv
    if not movies:
        print("no movies to save.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        for m in movies:
            row = {k: m.get(k, "") for k in FIELDNAMES}
            w.writerow(row)
    print(f"[save] wrote {len(movies)} rows to {filename}")

# === main flow ===
def main():
    if not API_KEY:
        print("error: API_KEY not available")
        return

    collected = []
    seen_ids = set()
    page = 1
    total_discovered = 0

    print(f"starting discover for genre id {comedy_genre_id} until we reach ~{target} unique movies.")

    while len(collected) < target and page <= max_discover_pages:
        print(f"discover page {page} ... (collected so far: {len(collected)})")
        data = discover_movies_by_genre(comedy_genre_id, page=page)
        results = data.get("results", [])
        if not results:
            print("no results returned for this page; stopping discover.")
            break

        total_discovered += len(results)
        for item in results:
            if len(collected) >= target:
                break
            movie_id = item.get("id")
            if not movie_id or movie_id in seen_ids:
                continue

            # fetch details and credits, pause between calls
            details = fetch_movie_details(movie_id)
            time.sleep(sleep_between_requests)
            credits = fetch_movie_credits(movie_id)
            time.sleep(sleep_between_requests)

            if not details:
                # if details fail skip
                continue

            # debug print for first few items to confirm vote_average looks normal
            if len(collected) < 5:
                print(f"[debug sample] {details.get('title')} -> vote_average = {details.get('vote_average')} (vote_count = {details.get('vote_count')})")

            genres_list = details.get("genres") or []
            genre_names = ", ".join([g.get("name") for g in genres_list if g.get("name")])

            budget = details.get("budget")
            revenue = details.get("revenue")
            vote_average = details.get("vote_average")
            vote_count = details.get("vote_count")
            runtime = details.get("runtime")
            original_language = details.get("original_language")
            popularity = details.get("popularity")
            top_actors = top_actors_from_credits(credits, 3)
            director = director_from_credits(credits)

            success_label, success_reason = classify_success(
                budget if budget and budget > 0 else None,
                revenue if revenue and revenue > 0 else None,
                vote_average,
                vote_count
            )

            row = {
                "tmdb_id": movie_id,
                "title": details.get("title"),
                "release_date": details.get("release_date", ""),
                "year": (details.get("release_date") or "")[:4] if details.get("release_date") else "",
                "original_language": original_language,
                "runtime": runtime,
                "genres": genre_names,
                "budget": budget,
                "revenue": revenue,
                "popularity": popularity,
                "vote_average": vote_average,
                "vote_count": vote_count,
                "director": director or "",
                "top_actors": ", ".join(top_actors),
                "overview": details.get("overview", ""),
                "success_label": success_label,
                "success_reason": success_reason
            }

            collected.append(row)
            seen_ids.add(movie_id)

            # save progress periodically
            if len(collected) % save_every == 0:
                save_movies_to_csv(collected)

        page += 1

    # final output save
    save_movies_to_csv(collected)
    print(f"finished. collected {len(collected)} unique movies (discovered {total_discovered} items across pages).")

if __name__ == "__main__":
    main()
