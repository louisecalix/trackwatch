import requests
from bs4 import BeautifulSoup

class Searching:
    def __init__(self, api_key_file='TrackWatch/apikey/tmdb_api_key'):
        self.api_key = self.read_api_key(api_key_file)
        # self.scraper = Scraping()

    def read_api_key(self, file_path):
        try:
            with open(file_path) as f:
                return f.read().strip()
        except FileNotFoundError: 
            print("API key file not found.")
            return None

    def search(self, title, year=None):
        if not self.api_key:
            print("API key is not available.")
            return None

        query = title.replace(' ', '%20')
        url = f'https://api.themoviedb.org/3/search/multi?api_key={self.api_key}&query={query}'

        if year:
            url += f'&year={year}&first_air_date_year={year}'


        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                for result in data['results']:
                    if result['media_type'] == 'movie':
                        search_type = 'Movie'
                        if year and 'release_date' in result and result['release_date'].startswith(str(year)):
                            movie_id = result['id']
                            tmdb_url = f'https://www.themoviedb.org/movie/{movie_id}'
                            print("TMDB URL:", tmdb_url)
                            return tmdb_url, search_type
                        elif not year:
                            movie_id = result['id']
                            tmdb_url = f'https://www.themoviedb.org/movie/{movie_id}'
                            print("TMDB URL:", tmdb_url)
                            return tmdb_url, search_type
                    elif result['media_type'] == 'tv':
                        search_type = 'Series'
                        if year and 'first_air_date' in result and result['first_air_date'].startswith(str(year)):
                            show_id = result['id']
                            tmdb_url = f'https://www.themoviedb.org/tv/{show_id}'
                            print("TMDB URL:", tmdb_url)
                            return tmdb_url, search_type
                        elif not year:
                            show_id = result['id']
                            tmdb_url = f'https://www.themoviedb.org/tv/{show_id}'
                            print("TMDB URL:", tmdb_url)
                            return tmdb_url, search_type
                print("No movie or TV show found in the results.")
            else:
                print("No results found.")
        else:
            print(f"Failed to retrieve search results from TMDB.\nStatus Code: {response.status_code}")

    

class Scraping:
    def scrape(self, url):
        site = url[0]
        response = requests.get(site)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # TITLE, YEAR
            title = soup.find('h2')
            if title:
                title_anchor = title.find('a')
                title_name = title_anchor.text.strip() if title_anchor else "Title not available"
                year_span = title.find('span', class_='tag release_date')
                year = year_span.text.strip() if year_span else "Year not available"
            else:
                title_name = "Title not available"
                year = "Year not available"

            # print(f'Title: {title_name}')
            # print(f'Year: {year}')


            # OVERVIEW
            overview = soup.find('div', class_='overview')
            if overview:
                overview_paragraph = overview.find('p')
                if overview_paragraph:
                    overview_text = overview_paragraph.text.strip()  
                    # print(f'Overview: {overview_text}')
                else:
                    print('Overview paragraph not found.')
                    overview_text = "Overview not available"
            else:
                overview_text = "Overview not available"

            # GENRES, RUNTIME
            fact = soup.find('div', class_='facts')
            if fact:
                genres_tag = fact.find('span', class_='genres')
                genres = genres_tag.text.strip() if genres_tag else "Genres not available"
                
                runtime_tag = fact.find('span', class_='runtime')
                runtime = runtime_tag.text.strip() if runtime_tag else "Runtime not available"

                # print(f'Genre: {genres}')
                # print(f'Runtime: {runtime}')
            else:
                genres = "Genres not available"
                runtime = "Runtime not available"

            # DIRECTOR
            people = soup.find('li', class_='profile')
            if people:
                director = people.find('p')
                if director:
                    director_text = director.find('a').text
                    # print(f'Director: {director_text}')
                else:
                    director_text = "Director not available"
                    # print(f'Director: {director_text}')
            else:
                director_text = "Director not available"
                # print(f'Director: {director_text}')

            # CAST
            casts = soup.find_all('li', class_='card')
            cast_list = []
            for cast in casts:
                cast_p = cast.find('p')
                if cast_p:
                    cast_name = cast_p.find('a').text
                    cast_list.append(cast_name)
                # else:
                    # print('Cast: Cast not available')

            cast_string = ', '.join(cast_list)
            # print(f'Cast: {cast_string}')

            # RATING
            rating = soup.find('div', class_='user_score_chart')
            rating_text = rating.get('data-percent') if rating else "Rating not available"
            # print(f'Rating: {rating_text}%')

            return title_name, year, overview_text, genres, runtime, director_text, cast_string, rating_text

        else:
            print(f'Failed. Status code: {response.status_code}')
            return None
        
