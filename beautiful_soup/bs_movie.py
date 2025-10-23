from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome()
driver.get("https://www.themoviedb.org/movie")


soup = BeautifulSoup(driver.page_source, 'html5lib')


# find the reject cookies button and click it
# reject_all_cookies_button = soup.find("button", { "class" : "onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon" })
# reject_all_cookies_button.click()
# time.sleep(2)  # wait for the page to load after cookies are rejected

page = soup.find_all('div', { "class" : "page_wrapper" })[0]
movies = page.find_all('div', { "class" : "card style_1"})
print(f"Found {len(movies)} movies.\n")

for movie in movies:
    h2_tag = movie.find('h2')
    a_tag = h2_tag.find('a')
    relative_url = a_tag['href']
    full_url = f"https://www.themoviedb.org{relative_url}"

    driver.get(full_url)
    inner_movie = inner_soup = BeautifulSoup(driver.page_source, 'html5lib')

    # TODO: scrape movie details here...
    title = None
    pg_rating = None
    date_and_country_of_release = None
    duration = None
    overview = None
    director = None
    actors = None
    original_title = None
    status = None
    original_language = None
    budget = None
    revenue = None
    movie_keywords = None

    # outer_container = inner_movie.find('div', { "class" : "title ott_false" })
    title = inner_movie.find('div', { "class" : "title ott_false" }).find('h2').find('a').text
    year = inner_movie.find('div', { "class" : "title ott_false" }).find('h2').find('span').text
    user_score = inner_movie.find('div', { "class" : "user_score_chart" }).get_attribute_list("data-percent")[0]
    pg_rating = inner_movie.find('span', { "class" : "certification" }).text.strip() if inner_movie.find('span', { "class" : "certification" }) else "Not Rated"
    release = inner_movie.find('span', { "class" : "release" }).text.strip() if inner_movie.find('span', { "class" : "release" }) else "No release date"
    genres = inner_movie.find('span', { "class" : "genres" }).text.strip() if inner_movie.find('span', { "class" : "genres" }) else "No genres"
    duration = inner_movie.find('span', { "class" : "runtime" }).text.strip() if inner_movie.find('span', { "class" : "runtime" }) else "No duration"
    overview = inner_movie.find('div', { "class" : "overview" }).find('p').text.strip() if inner_movie.find('div', { "class" : "overview" }) else "No overview"
    side_facts = inner_movie.find('section', { "class" : "facts left_column" })
    original_title = side_facts.find('p', { "class" : "wrap" }).text if side_facts.find('p', { "class" : "wrap" }) else "No original title"
    status = side_facts.find_all('p')[1].text.replace("Status", "", 1).strip() if len(side_facts.find_all('p')) > 1 and original_title != "No original title" else side_facts.find_all('p')[0].text.replace("Status", "", 1).strip()
    # budget = side_fact
    # revenue = side_fact

    # movie_keywords = inner_movie.find("section", { "class" : "keywords right_column" }).find("ul").find_all("li") if inner_movie.find("section", { "class" : "keywords right_column"}) else "No keywords"
    # movies_keywords_list = [keyword.find("a").text for keyword in movie_keywords]

    keywords_section = inner_movie.find("section", {"class": "keywords right_column"})

    if keywords_section:
        ul_tag = keywords_section.find("ul")
        if ul_tag:  # movie has keywords
            movie_keywords = [li.get_text(strip=True) for li in ul_tag.find_all("li")]
        else:  # no <ul> → movie has no keywords
            movie_keywords = ["No keywords"]
    else:
        movie_keywords = ["No keywords"]


    # year = inner_movie.find('h2', { "class" : "9" }).find('span').text
    print("title: ", title)
    print("year: ", year)
    print("user score: ", user_score)
    print("pg_rating: ", pg_rating)
    print("release:", release)
    print("genres:", genres)
    print("duration:", duration)
    print("overview:", overview)
    print("original_title:", original_title)
    print("status:", status)
    print("movie keywords: ", movie_keywords)
    print(("-------------------------------------------------\n"))


driver.quit()

# load the initial page of movies
# access the details of each movie from the page and scrape the required information
# write the scraped information to a row in a CSV file

'''
title - done
year - done
user score - done
pg_rating - done
release - done
genres - done
duration - done
overview - done
director
actors
original title - done
status - done
original language - done
budget
revenue
movie_keywords
'''


'''
DevTools listening on ws://127.0.0.1:54290/devtools/browser/e689f49d-e44e-4f94-9377-9a31d3ab4b75
Found 20 movies.

<div class="card style_1">
 <div class="image">
  <div class="wrapper glyphicons_v2 picture grey no_image_holder">
   <a class="image" href="/movie/1156594-culpa-nuestra" title="Our Fault">
    <img alt="Our Fault" class="poster w-full" loading="lazy" src="https://media.themoviedb.org/t/p/w220_and_h330_face/yzqHt4m1SeY9FbPrf
Z0C2Hi9x1s.jpg" srcset="https://media.themoviedb.org/t/p/w220_and_h330_face/yzqHt4m1SeY9FbPrfZ0C2Hi9x1s.jpg 1x, https://media.themoviedb
.org/t/p/w440_and_h660_face/yzqHt4m1SeY9FbPrfZ0C2Hi9x1s.jpg 2x"/>
   </a>
  </div>
  <div class="options" data-id="1156594" data-media-type="movie" data-object-id="64c12f901cfe3a0eb30bf2b5" data-role="tooltip">
   <a aria-label="View Item Options" class="no_click" href="#">
    <div class="glyphicons_v2 circle-more white">
    </div>
   </a>
  </div>
 </div>
 <div class="content">
  <div class="consensus tight">
   <div class="outer_ring">
    <div class="user_score_chart 64c12f901cfe3a0eb30bf2b5" data-bar-color="#21d07a" data-percent="77" data-track-color="#204529">
     <div class="percent">
      <span class="icon icon-r77">
      </span>
     </div>
     <canvas height="40" style="height: 34px; width: 34px;" width="40">
     </canvas>
    </div>
   </div>
  </div>
  <h2>
   <a href="/movie/1156594-culpa-nuestra" title="Our Fault">
    Our Fault
   </a>
  </h2>
  <p>
   Oct 15, 2025
  </p>
 </div>
 <div class="hover 1156594">
 </div>
</div>
'''
