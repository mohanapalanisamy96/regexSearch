import re
from typing import List, Dict
from flask import Flask
from flask_cors import CORS 
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

def load_movies_from_directory(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Regex-based search function
def search_content(userInput: str, directory: List[Dict]) -> List[Dict]:
    tokens = userInput.strip().split()
    pattern = ''.join(f"(?=.*{re.escape(token)})" for token in tokens)
    regex = re.compile(pattern, re.IGNORECASE)

    matched_content = []

    for movie in directory:
        searchable_text = (
            movie["title"] + " " +
            movie["plot"] + " " +
            " ".join(movie["cast"]) + " " +
            " ".join(movie["genres"]) + " " +
            movie["director"]
        )
        if regex.search(searchable_text):
            matched_content.append(movie)

    return matched_content

# Find related content by cast and crew if unavailable
def find_related_content(base_movie: Dict, directory: List[Dict]) -> List[Dict]:
    related_content = []
    base_cast = set(base_movie["cast"])
    base_director = base_movie["director"]

    for entry in directory:
        if entry["title"] == base_movie["title"]:
            continue
        if entry["available"] and (base_cast.intersection(set(entry["cast"])) or entry["director"] == base_director):
            related_content.append(entry)
    return related_content

# Example usage
if __name__ == "__main__":
    print("Regex-Enhanced Search Engine\n")
    user_query = input("Enter your search query (as regex): ")
    directory = load_movies_from_directory("movies_directory.json")
    matched_results = search_content(user_query, directory)
    movie_found = False

    if not matched_results:
        print("No matches found. Here are some suggestions based on others have also liked")
        for result in directory:
            if result["available"]:
                print(f"\nTitle: {result['title']}")
                print(f"Year: {result['release_year']}")
                print(f"Cast: {', '.join(result['cast'])}")
                print(f"Director: {result['director']}")
                print(f"Genres: {', '.join(result['genres'])}")
                print(f"Plot: {result['plot']}\n")
    else:
        for result in matched_results:
            if result["available"]:
                movie_found = True
                print(f"\nTitle: {result['title']}")
                print(f"Year: {result['release_year']}")
                print(f"Cast: {', '.join(result['cast'])}")
                print(f"Director: {result['director']}")
                print(f"Genres: {', '.join(result['genres'])}")
                print(f"Plot: {result['plot']}\n")
            elif movie_found == False:
                print(f"\n'{result['title']}' is not currently available to stream.")
                related = find_related_content(result, directory)
                if related:
                    print("Here are some movies with the same cast or director:")
                    for r in related:
                        print(f"\nTitle: {r['title']}")
                        print(f"Year: {r['release_year']}")
                        print(f"Cast: {', '.join(r['cast'])}")
                        print(f"Director: {r['director']}")
                        print(f"Genres: {', '.join(r['genres'])}")
                        print(f"Plot: {r['plot']}\n")
                else:
                    print("No related movies found. Here are some suggestions based on others have also liked")
                    for result in directory:
                        if result["available"]:
                            print(f"\nTitle: {result['title']}")
                            print(f"Year: {result['release_year']}")
                            print(f"Cast: {', '.join(result['cast'])}")
                            print(f"Director: {result['director']}")
                            print(f"Genres: {', '.join(result['genres'])}")
                            print(f"Plot: {result['plot']}\n")

