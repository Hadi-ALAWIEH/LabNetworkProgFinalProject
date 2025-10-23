import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'

def fetch_genres():
    """Fetch the genre list from TMDb."""
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        return {genre['id']: genre['name'] for genre in genres}
    else:
        print("Error fetching genres:", response.status_code)
        return {}

def fetch_top_comedy_movies(page=1):
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres=35&sort_by=vote_average.desc&page={page}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print("Error fetching data:", response.status_code)
        return []

def save_movies_to_csv(movies, filename='movies.csv'):
    if not movies:
        print("No movies to save.")
        return
    
    keys = movies[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(movies)
    print(f"Wrote {len(movies)} movies to {filename}.")
    
def fetch_movie_details(movie_id):
    """Fetch detailed movie information including accurate ratings."""
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching movie details:", response.status_code)
        return None

def main():
    all_movies = []
    target_movies = 1000  # Set your target for total movies
    total_pages = 50      # Adjust this if needed

    # Fetch genres mapping
    genres_mapping = fetch_genres()
    
    for page in range(1, total_pages + 1):
        print(f"Fetching page {page}...")
        movies = fetch_top_comedy_movies(page)
        
        if not movies:
            print("No more movies found.")
            break
        
        all_movies.extend(movies)

        if len(all_movies) >= target_movies:
            all_movies = all_movies[:target_movies]
            break

    movie_data = []
    for movie in all_movies:
        # Fetch detailed movie information for accurate ratings
        detailed_movie = fetch_movie_details(movie['id'])

        if detailed_movie:
            # Map genre IDs to names
            genre_names = [genres_mapping.get(genre_id, "Unknown Genre") for genre_id in detailed_movie.get('genre_ids', [])]

            movie_data.append({
                "title": detailed_movie['title'],
                "year": detailed_movie['release_date'][:4],
                "rating": detailed_movie['vote_average'],  # Use the accurate rating
                "description": detailed_movie.get('overview', 'No description available'),
                "genres": ", ".join(genre_names)  # Join genre names into a string
            })
    
    save_movies_to_csv(movie_data)

if __name__ == "__main__":
    main()