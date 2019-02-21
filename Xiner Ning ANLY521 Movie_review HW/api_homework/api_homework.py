import argparse
import tmdbsimple as tmdb
import argparse
import requests
import time
import re


def main(api_key, output_file):
    """Use tmdbsimple to create a dataset with the reviews from exactly 100 movies.
    Each line of the tsv contains <movie_id>\t<author_id>\t<review_string> .
    tsvchecker.py confirms that your file is readable and contains data for exactly 100 movies. """
    tmdb.API_KEY = api_key
   
    # find 100 valid movie_id
    i=1
    movie_id=[]
    while (len(movie_id)<100): # keep trying until it works
        try: # only things that might cause HTTP error belong in the "try"
            movie = tmdb.Movies(i)  # this is one request
            response=movie.info()
            reviews = movie.reviews()
            review_list = reviews['results']
            if (review_list!=[]):
                movie_id.append(i) # only append those with reviews
            i=i+1
        except requests.HTTPError:
            print("invalid movie id")
            i=i+1
            time.sleep(0.3)  # now we have a list of valid movie id
        
    f= open(output_file,"w+",encoding="utf-8")
    i=0
    for i in range(0,len(movie_id)):
        while True: # keep trying until it works
            try: # only things that might cause HTTP error belong in the "try"
                movie = tmdb.Movies(movie_id[i])  # this is one request
                reviews = movie.reviews() # one request
                break
            except requests.HTTPError:
                print("HTTPError, waiting 3 seconds")
                time.sleep(0.3)
        review_list = reviews['results']
        for review_dict in review_list:
            auth = review_dict['author']
            text = review_dict['content']
            text=re.sub(r'\n',' ',text)
            text=re.sub(r'\t',' ',text)
            text=re.sub(r'\r',' ',text)
        f.write(f"{movie_id[i]}\t{auth}\t{text}\n")
        i=i+1
    f.close()





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--key_file", type=str, default="api_key.txt",
                        help="text file containing API key")
    parser.add_argument("--output_file", type=str, default="tmdb_dataset.tsv",
                        help="tsv: movie, author, review")
    args = parser.parse_args()

    with open(args.key_file, 'r') as key_path:
        key = key_path.read().strip()
    main(key, args.output_file)