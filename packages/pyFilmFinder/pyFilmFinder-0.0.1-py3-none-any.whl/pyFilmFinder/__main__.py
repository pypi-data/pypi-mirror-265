import os
import argparse
from dotenv import load_dotenv
from finder import Finder


def main():
    """
    Entry point for the Film Finder CLI application.
    """
    finder = Finder()
    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        while True:
            api_key = input("Enter your API key: ")
            finder.api_key = api_key
            if finder.validate_api_key():
                with open(".env", "w", encoding="utf-8") as f:
                    f.write(f"API_KEY={finder.api_key}\n")
                break
            print("Invalid API key. Please provide a valid API key.")

    parser = argparse.ArgumentParser(description="Film Finder CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Command to find films
    find_parser = subparsers.add_parser(
        "find",
        help="Find films based on specified genre(s), cast, and optionally a release year.",
        description="Find films based on specified genres, cast, and optionally a release year.",
    )
    # TODO: allow multiple genres
    find_parser.add_argument("--genres", default=None, help="filter by genres")
    # TODO: allow multiple cast memebers (directors and actors)
    find_parser.add_argument("--cast", default=None, help="filter by cast members")
    # TODO: allow user to input decade in place of year
    find_parser.add_argument("--year", default=None, help="filter by year")

    # Command to search films
    search_parser = subparsers.add_parser(
        "search",
        help="Search for films based on a keyword.",
        description="Search for films based on a keyword.",
    )
    search_parser.add_argument(
        "keyword",
        help="Specify a keyword to search for. The search will return films related to this keyword.",
    )

    # Command to find similar films
    similar_parser = subparsers.add_parser(
        "similar",
        help="Find films similar to the specified film.",
        description="Find films that are similar to a specified film.",
    )
    similar_parser.add_argument(
        "film_id",
        type=int,
        help="ID of the film for which to find similar films. Use the 'search' command to find the film ID.",
    )

    # Command to get details of a film
    details_parser = subparsers.add_parser(
        "details",
        help="Retrieve detailed information about a specified film.",
        description="Retrieve detailed information about a specified film.",
    )
    details_parser.add_argument(
        "film_id",
        type=int,
        help="ID of the film for which to retrieve details. Use the 'search' command to find the film ID.",
    )

    args = parser.parse_args()

    if args.command == "search":
        print(finder.search_films(args.keyword))
    elif args.command == "find":
        print(finder.find_films(args.genres, args.cast, args.year))
    elif args.command == "similar":
        print(finder.find_similar(args.film_id))
    elif args.command == "details":
        print(finder.get_details(args.film_id))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
