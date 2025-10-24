what was the problem
we scraped tmdb using the discover endpoint and then wrote results to csv, but all ratings in our csv showed as `10`. that turned out to be either:
- we read the wrong field or endpoint (discover vs details have different structures), or
- we had partial/error responses that looked like constants when written to csv, or
- excel/text viewer was hiding the real values.

what i fixed
- changed the script to fetch **details** for each movie (the details endpoint contains accurate `vote_average`, `budget`, `revenue`, runtime, and genres).
- added credits calls to get top actors and director.
- replaced page-based stop with a target count (`target = 1000`) so the script stops after collecting ~1000 unique movies.
- deduplicates by tmdb id to avoid repeats.
- prints debug samples for the first few movies so you can verify ratings while it runs.
- added retries, polite sleeps, and periodic saves to make the scraper robust and resumable.
- added a simple success classifier that uses budget/revenue and user score to label movies (blockbuster/hit/moderate/flop/unknown).
