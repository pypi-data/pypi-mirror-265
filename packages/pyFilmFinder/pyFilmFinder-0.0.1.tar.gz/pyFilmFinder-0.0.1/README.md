# pyFilmFinder

![CI / CD](https://github.com/software-students-spring2024/3-python-package-exercise-mjet/actions/workflows/build.yaml/badge.svg)

## Project Description

**pyFilmFinder** is a Python package designed to simplify the process of discovering and exploring films. Leveraging TMDB (The Movie Database), the package delivers personalized recommendations, enhancing the film-viewing experience by helping users discover films that align with their unique tastes and preferences.

### Features

* Fetch a list of films based on specified genres, cast, and release year.
* Search for films based on a specified keyword.
* Fetch a list of films similar to the specified film.
* Fetch detailed information about the specified film.

## Installation

You can install the package via pip:

```
pip3 install pyfilmfinder
```

## Usage

Once installed, you can call `pyfilmfinder` from the command line with the desired command and flags.

### Find Films

The find command has three optional arguments:

1. genres: Specifies the genre(s) of the films. This can be a single genre or a comma-separated list of genres. Available options are action, adventure, animation, comedy, documentary, drama, family, fantasy, history, horror, music, mystery, romance, science-fiction, thriller, tv-movie, war, western.

1. cast: Specifies the cast of the films. This can be the name of an actor/actress. For multiple cast members, separate their names with commas.

1. year: Specifies the release year of the films.

Example usage:

```
python3 src/pyFilmFinder find
```

This command will fetch a list of films. <!--that belong to the action and comedy genres, featuring Tom Hanks, and released in the year 1994.-->

### Search Keyword

The search command takes one argument:

1. keyword: Specifies the keyword to search for films.

Example usage:

```
python3 src/pyFilmFinder search "LoTR"
```

This command will search for films related to "LOTR".

### Find Similar Films

The similar command takes one argument:

1. film_id: Specifies the ID of the film to find similar movies for.

Example usage:

```
python3 src/pyFilmFinder similar 12
```

This command will fetch a list of movies similar to the film with the ID 12.

### Film Details

The details command takes one argument:

1. film_id: Specifies the ID of the film to fetch detailed information for.

Example usage:

```
python3 src/pyFilmFinder details 693134
```

This command will fetch detailed information about the film with the ID 693134.
