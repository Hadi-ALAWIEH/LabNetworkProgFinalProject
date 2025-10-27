from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Define the CSV columns (same structure as your Selenium version)
columns = [
    "title",
    "release_date",
    "year",
    "original_language",
    "runtime",
    "genres",
    "budget",
    "revenue",
    "vote_average",
    "director",
    "top_actors",
    "overview",
    "pg_rating",
    "original_title",
    "movie_keywords"
]

driver = webdriver.Chrome()

# open CSV file for writing
with open("tmdb_movies_bs4.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    # scrape multiple pages
    for page_counter in range(1, 10):  # adjust page range here
        base_url = f"https://www.themoviedb.org/movie?page={page_counter}"
        driver.get(base_url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html5lib")
        page = soup.find_all("div", {"class": "page_wrapper"})[0]
        movies = page.find_all("div", {"class": "card style_1"})
        print(f"\n=== Page {page_counter} | Found {len(movies)} movies ===\n")

        for i, movie in enumerate(movies):
            h2_tag = movie.find("h2")
            a_tag = h2_tag.find("a")
            relative_url = a_tag["href"]
            full_url = f"https://www.themoviedb.org{relative_url}"

            driver.get(full_url)
            inner_movie = BeautifulSoup(driver.page_source, "html5lib")

            try:
                # movie info extraction (unchanged)
                title = inner_movie.find("div", {"class": "title ott_false"}).find("h2").find("a").text
                year = inner_movie.find("div", {"class": "title ott_false"}).find("h2").find("span").text
                user_score = inner_movie.find("div", {"class": "user_score_chart"}).get_attribute_list("data-percent")[0]
                pg_rating = inner_movie.find("span", {"class": "certification"}).text.strip() if inner_movie.find("span", {"class": "certification"}) else "Not Rated"
                release = inner_movie.find("span", {"class": "release"}).text.strip() if inner_movie.find("span", {"class": "release"}) else "No release date"
                genres = inner_movie.find("span", {"class": "genres"}).text.strip() if inner_movie.find("span", {"class": "genres"}) else "No genres"
                duration = inner_movie.find("span", {"class": "runtime"}).text.strip() if inner_movie.find("span", {"class": "runtime"}) else "No duration"
                overview = inner_movie.find("div", {"class": "overview"}).find("p").text.strip() if inner_movie.find("div", {"class": "overview"}) else "No overview"

                side_facts = inner_movie.find("section", {"class": "facts left_column"})
                original_title = side_facts.find("p", {"class": "wrap"}).text if side_facts.find("p", {"class": "wrap"}) else "No original title"
                status = side_facts.find_all("p")[1].text.replace("Status", "", 1).strip() if len(side_facts.find_all("p")) > 1 and original_title != "No original title" else side_facts.find_all("p")[0].text.replace("Status", "", 1).strip()
                original_language = side_facts.find_all("p")[1].text.replace("Original Language", "", 1).strip() if len(side_facts.find_all("p")) > 1 and original_title == "No original title" else side_facts.find_all("p")[2].text.replace("Original Language", "", 1).strip()
                budget = side_facts.find_all("p")[2].text.replace("Budget", "", 1).strip() if len(side_facts.find_all("p")) > 2 else "No budget"
                revenue = side_facts.find_all("p")[3].text.replace("Revenue", "", 1).strip() if len(side_facts.find_all("p")) > 3 else "No revenue"

                director = inner_movie.find("ol", {"class": "people no_image"}).find("li").find("p").find("a").text

                # keywords
                keywords_section = inner_movie.find("section", {"class": "keywords right_column"})
                if keywords_section:
                    ul_tag = keywords_section.find("ul")
                    movie_keywords = [li.get_text(strip=True) for li in ul_tag.find_all("li")] if ul_tag else ["No keywords"]
                else:
                    movie_keywords = ["No keywords"]

                # top 3 stars
                top_stars = inner_movie.find("ol", {"class": "people scroller"}).find_all("li", limit=3)
                top_stars_list = [top_star.find("p").find("a").text for top_star in top_stars]

                # write movie data to CSV
                writer.writerow({
                    "title": title,
                    "release_date": release,
                    "year": year,
                    "original_language": original_language,
                    "runtime": duration,
                    "genres": genres,
                    "budget": budget,
                    "revenue": revenue,
                    "vote_average": user_score,
                    "director": director,
                    "top_actors": ", ".join(top_stars_list),
                    "overview": overview,
                    "pg_rating": pg_rating,
                    "original_title": original_title,
                    "movie_keywords": ", ".join(movie_keywords)
                })

                print(f"✔ Saved: {title} ({year})")

            except Exception as e:
                print(f"❌ Error scraping movie {i+1} on page {page_counter}: {e}")

driver.quit()
print("\n✅ Scraping complete! All movies saved to tmdb_movies_bs4.csv")
