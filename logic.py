from webscraping import Searching, Scraping
from tkinter import *
import customtkinter

class WatchList:
    def __init__(self) -> None:
        self.to_watch = []
        self.watched = []
        self.watching = []
        self.search = Searching()
        self.scraping = Scraping()

    def add_to_watch(self, title):
        self.to_watch.append(title)
        print(f'Added to watchlist [TO WATCH]: {title}')

    def add_to_watching(self, title):
        self.watched.append(title)
        print(f'Added to watchlist [WATCHING]: {title}')

    def add_to_watched(self, title):
        self.watching.append(title)
        print(f'Added to watchlist [WATCHED]: {title}')


    def display_list(self, list_name):
        list_map = {
            'to_watch': self.to_watch,
            'watched': self.watched,
            'watching': self.watching
        }

        if list_name in list_map:
            print(f"\n{list_name} list:")
            for item in list_map[list_name]:
                print(item)
        else:
            print('Invalid list name')


class Movie:
    def __init__(self, title, year, overview, genres, runtime, director, cast, rating) -> None:
        self.title = title
        self.year = year
        self.overview = overview
        self.genres = genres
        self.runtime = runtime
        self.director = director
        self.cast = cast
        self.rating = rating

    def get_details(self):
        return {
            'Title': self.title,
            'Year': self.year,
            'Overview': self.overview,
            'Genre': self.genres,
            'Runtime': self.runtime,
            'Director': self.director,
            'Cast': ', '.join(self.cast),
            'Rating': self.rating
        }

class Series:
    def __init__(self, title, year, overview, genres, runtime, director, cast, rating) -> None:
        self.title = title
        self.year = year
        self.overview = overview
        self.genres = genres
        self.runtime = runtime
        self.director = director
        self.cast = cast
        self.rating = rating

    def get_details(self):
        return {
            'Title': self.title,
            'Year': self.year,
            'Overview': self.overview,
            'Genre': self.genres,
            'Runtime': self.runtime,
            'Director': self.director,
            'Cast': ', '.join(self.cast),
            'Rating': self.rating
        }


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.watchlist = WatchList()

    def check_password(self, password):
        return self.password == password

class WatchListManager:
    def __init__(self) -> None:
        self.watchlist = WatchList()
        self.users = {}

    def create_account(self, username, password):
        if username in self.users:
            return False
        user = User(username, password)
        self.users[username] = user
        return True

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.check_password(password):
            return user
        else:
            return None
        
    def run(self, title, list_name, year=None):
        print(f"Running search with title: {title}, year: {year}")

        search_result = self.watchlist.search.search(title, year)
        if search_result:
            tmdb_url, search_type = search_result
            print(f"Found {search_type} at {tmdb_url}")

            details = self.watchlist.scraping.scrape((tmdb_url,))
            if details:
                title_name, year, overview_text, genres, runtime, director_text, cast_string, rating_text = details
                print(f"Scraped details: {details}")

                if search_type == 'Movie':
                    movie = Movie(title_name, year, overview_text, genres, runtime, director_text, cast_string.split(', '), rating_text)
                    if list_name == 'to_watch':
                        self.watchlist.add_to_watch(title_name)
                    elif list_name == 'watching':
                        self.watchlist.add_to_watching(title_name)
                    elif list_name == 'watched':
                        self.watchlist.add_to_watched(title_name)
                    return movie.get_details()

                elif search_type == 'Series':
                    series = Series(title_name, year, overview_text, genres, runtime, director_text, cast_string.split(', '), rating_text)
                    if list_name == 'to_watch':
                        self.watchlist.add_to_watch(title_name)
                    elif list_name == 'watching':
                        self.watchlist.add_to_watching(title_name)
                    elif list_name == 'watched':
                        self.watchlist.add_to_watched(title_name)
                    return series.get_details()
                
        else:
            print('No result found')
            return None




        self.watchlist.display_list('to_watch')
        self.watchlist.display_list('watching')
        self.watchlist.display_list('watched')