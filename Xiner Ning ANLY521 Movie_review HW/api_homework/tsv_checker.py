import csv
import numpy as np
from collections import defaultdict


tsv_file = 'example_movie.tsv'

movie_to_auth = defaultdict(list)
auth_to_movie = defaultdict(list)
with open(tsv_file,'r') as tsv_file:
    tsvin = csv.reader(tsv_file, delimiter='\t')
    for movie_id, author, review_text in tsvin: # will crash on lines of wrong length
        movie_to_auth[movie_id].append(author)
        auth_to_movie[author].append(movie_id)

num_movies = len(movie_to_auth)
reviews_per_movie = np.asarray([len(auth_list) for auth_list in movie_to_auth.values()])
print(f"Found {num_movies} movies (must be exactly 100)")
total_reviews = sum(reviews_per_movie) # all reviews counted
print(f"Found {total_reviews} reviews (can be any number)")

print(f"Most per movie: {reviews_per_movie.max()}, least per movie {reviews_per_movie.min()}, mean {reviews_per_movie.mean():.02}")

num_authors = len(auth_to_movie)
reviews_per_author = np.asarray([len(movie_list) for movie_list in auth_to_movie.values()])
print(f"Found {num_authors} authors (can be any number)")
print(f"Most per author: {reviews_per_author.max()}, least per author {reviews_per_author.min()}, mean {reviews_per_author.mean():.02}")