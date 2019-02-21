# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 11:52:56 2019

@author: shera
"""
import tmdbsimple as tmdb
import argparse
import requests
import time
import re

# import API key
parser = argparse.ArgumentParser()
parser.add_argument("--key_file", type=str, default="api_key.txt",
                    help="text file containing API key")
args = parser.parse_args()

with open(args.key_file, 'r') as key_path:
    key = key_path.read().strip()
tmdb.API_KEY = key

# find 100 valid movie_id
i=1
movie_id=[]
while (len(movie_id)<100): # keep trying until it works
    try: # only things that might cause HTTP error belong in the "try"
        movie = tmdb.Movies(i)  # this is one request
        #reviews = movie.reviews() # one request
        #break
        response=movie.info()
        #print(response)
        i=i+1
        movie_id.append(i)
        #break
        
    except requests.HTTPError:
        print("invalid movie id")
        i=i+1
        #time.sleep(5)

f= open("movie.tsv","w+")
for i in range(0,(len(movie_id)-90)):
    while True: # keep trying until it works
        try: # only things that might cause HTTP error belong in the "try"
            movie = tmdb.Movies(movie_id[i])  # this is one request
            reviews = movie.reviews() # one request
            break
        except requests.HTTPError:
            print("HTTPError, waiting 3 seconds")
            time.sleep(3)
    #review_list = reviews['results']
    #for review_dict in review_list:
        #auth = review_dict['author']
        #text = review_dict['content']
        #text=re.sub(r'\n',' ',text)
        #text=re.sub(r'\t',' ',text)
    print(movie.id)
        
f.close()
i=0
while True: # keep trying until it works
    try: # only things that might cause HTTP error belong in the "try"
        movie = tmdb.Movies(movie_id[i])  # this is one request
        reviews = movie.reviews() # one request
        print(movie.id)
    except requests.HTTPError:
        print("HTTPError, waiting 5 seconds")
        time.sleep(5)
    i=i+1
auth='Shera'   
f= open("movie.tsv","w+")
f.write('%d' % movie_id[0]+'\t'+auth )
f.close()