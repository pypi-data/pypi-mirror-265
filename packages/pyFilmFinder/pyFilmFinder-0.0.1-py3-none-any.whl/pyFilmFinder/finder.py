import os
import requests
from dotenv import load_dotenv


class Finder:
    """
    A utility class for fetching information about films from The Movie Database (TMDB) API.
    """

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.base_url = "https://api.themoviedb.org/3/"

    def validate_api_key(self) -> bool:
        """
        Validate the API key by making a test request to the API endpoint.
        """
        api_url = f"{self.base_url}authentication?api_key={self.api_key}"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch films from API: {e}.")
            return False

    def find_films(self, genres: str = None, cast: str = None, year: int = None) -> str:
        """
        Fetches a list of films based on specified genres, cast, and release year.
        """
        # TODO: convert incoming genre(s) to their corresponding id(s)
        # genres_id = {
        #     "action": 28,
        #     "adventure": 12,
        #     "animation": 16,
        #     "comedy": 35,
        #     "documentary": 99,
        #     "drama": 18,
        #     "family": 10751,
        #     "fantasy": 14,
        #     "history": 36,
        #     "horror": 27,
        #     "music": 10402,
        #     "mystery": 9648,
        #     "romance": 10749,
        #     "science-fiction": 878,
        #     "thriller": 53,
        #     "tv-movie": 10770,
        #     "war": 10752,
        #     "western": 37,
        # }
        api_url = f"{self.base_url}discover/movie?language=en-US&api_key={self.api_key}"

        # TODO: validate params
        if genres:
            api_url += f"&with_genres={genres}"
        if cast:
            api_url += f"&with_cast={cast}"
        if year:
            api_url += f"&primary_release_year={year}"

        return self.get_films(api_url)

    def search_films(self, keyword: str) -> str:
        """
        Searches for films based on a specified keyword.
        """
        api_url = f"{self.base_url}search/movie?language=en-US&page=1&query={keyword}&api_key={self.api_key}"
        return self.get_films(api_url)

    def find_similar(self, film_id: int) -> str:
        """
        Fetches a list of movies similar to the specified movie.
        """
        api_url = (
            f"{self.base_url}movie/{film_id}/recommendations?api_key={self.api_key}"
        )
        return self.get_films(api_url)

    def get_details(self, film_id: int) -> str:
        """
        Fetches detailed information about the specified film.
        """
        api_url = f"{self.base_url}movie/{film_id}?language=en-US&api_key={self.api_key}"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            details = response.json()
            # TODO: parse response for desired fields
            title = details.get("title", "")
            film_id = details.get("id", "")
            vote_average = details.get("vote_average", "")
            overview = details.get("overview", "")
            release_date = details.get("release_date", "")
            tagline = details.get("tagline", "")
            released = details.get("status", "")
            budget = details.get("budget", "")
            popularity = details.get("popularity", "")
            revenue = details.get("revenue", "")
            genre_names = [genre["name"] for genre in details["genres"]]
            production_companies = [
                company["name"] for company in details["production_companies"]
            ]
            details_formatted = "======================================================================================"
            details_formatted += f"\nTitle: {title}\nReleased: {release_date}\n(ID: {film_id})\nGenres: {genre_names}\nProduction Companies: {production_companies}\nStatus: {released}\nBudget: {budget}\nVote Average: {vote_average}\nPopularity Score: {popularity}\nRevenue: {revenue}\n"
            details_formatted += f"Description: {overview}\nTagline: {tagline}\n\n"
            details_formatted += "======================================================================================"
            return details_formatted
        except requests.exceptions.RequestException as e:
            return f"Failed to fetch films from API: {e}."

    def format_film(self, film: dict) -> str:
        """
        Format the given film information into a readable string.
        """
        title = film.get("title", "")
        film_id = film.get("id", "")
        vote_average = film.get("vote_average", "")
        overview = film.get("overview", "")
        release_date = film.get("release_date", "")
        formatted_film = f"Title: {title} Released: {release_date} (ID: {film_id}) Vote Average: {vote_average}\n"
        formatted_film += f"Description: {overview}\n\n"
        return formatted_film

    def get_films(self, api_url: str) -> str:
        """
        Retrieve films from the specified API URL and return them as a formatted string.
        """
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            films = response.json()
            if films.get("total_results", 0) == 0:
                return "No results found."
            films = films.get("results", [])
            formatted_films = ""
            count = 0
            for film in films:
                if count >= 5:
                    break
                if (
                    not film.get("title")
                    or not film.get("vote_average")
                    or not film.get("overview")
                    or film.get("popularity", 0) < 10
                    or not film.get("release_date")
                ):
                    continue
                formatted_films += self.format_film(film)
                count += 1
            return formatted_films
        except requests.exceptions.RequestException as e:
            return f"Failed to fetch films from API: {e}."
