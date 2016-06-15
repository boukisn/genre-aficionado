from tqdm import tqdm 	# Timing iterators
import unicodedata		# Writing artist names in the correct format
import threading		# Downloading images on multiple threads
import spotipy 			# Spotify API
import urllib			# Library for downloading images
import sys
import os

# Global variables
spotify = spotipy.Spotify()
genres = []
genresToArtists = {}

# Download specified image and place within specified genre's foloder
def fetch_url(url,genre,counter):
	try:
		urllib.urlretrieve(url, "genre_images/" + genre + "/" + str(counter) + ".jpg")
	except:
		return

# Create threads for each image url to download
def download_urls(urls, genre):
	threads = [threading.Thread(target=fetch_url, args=(urls[i],genre,i)) for i in range(len(urls))]
	for thread in threads:
	    thread.start()
	for thread in tqdm(threads):
	    thread.join()

# Load genres from text file into list
def load_genres(filename='genres.txt'):
	with open(filename) as f:
		genres = f.readlines()
	return genres

# Generate directories for each genre
def generate_directories(genres):
	for genre in tqdm(genres):
		genre = genre[:-1] # Shave off newline
		if not os.path.exists("genre_images/" + genre):
			os.makedirs("genre_images/" + genre)

# Map each genre to a list of artists associated with that genre
def generate_dictionary(genres):
	genresToArtists = {}
	for genre in tqdm(genres):
		genre = genre[:-1] # Shave off newline
		currentOffset = 0
		artistsPresent = True
		limit = 30
		genresToArtists[genre] = []
		while artistsPresent:
			results = spotify.search(q='genre:\"' + genre + '\"', type='artist', limit=limit, offset=currentOffset)
			if results:
				items = results['artists']['items']
				if len(items) > 0 and len(items) <= limit:
					for item in items:
						genresToArtists[genre].append(item['name'])
					if len(items) == limit:
						currentOffset += limit
					elif len(items) > 0 and len(items) < limit:
						currentOffset += len(items)
				else:
					artistsPresent = False
	return genresToArtists

#  Write mapping of genres to artists to a text file
def write_genre_artist_map(genresToArtists, filename='genres_to_artists.txt'):
	f = open(filename, 'w+')
	for genre in tqdm(genresToArtists):
		if not os.path.exists("genre_images/" + genre):
			os.makedirs("genre_images/" + genre)
		genresToArtistsString = genre.replace(":", " ") + ":\""
		for artist in genresToArtists[genre]:
			genresToArtistsString += artist + "\",\""
		genresToArtistsString = genresToArtistsString[:-2] + "\n"
		f.write(genresToArtistsString.encode('utf8'))
	f.close()

# Read from text file which maps genres to artists and download collection of album art for each artist,
# placing images in their respective image directory
def download_album_art(filename='genres_to_artists.txt', size=2):
	with open(filename) as f:
	    genreInfoList = f.readlines()

	for genre in tqdm(genreInfoList):
		urls = []
		currGenrePair = genre.split(':', 1)
		if len(currGenrePair) > 1:
			if len(os.listdir("genre_images/" + currGenrePair[0] + "/")) <= 1:
				artists = currGenrePair[1].split('","')
				artists[0] = artists[0][1:] 	# Remove " from first element
				artists[-1] = artists[-1][:-2] 	# Remove "\n from last element
				for artist in artists:
					results = None
					try:
						results = spotify.search(q='artist:\"' + artist + '\"', type='album', limit=50, offset=0)
					except:
						pass
					if results:
						if len(results["albums"]["items"]) > 0:
							for album in results["albums"]["items"]:
								if len(album["images"]) == 3:
									url = album["images"][size]["url"]
									urls.append(url)
				download_urls(urls, currGenrePair[0])

## 1. Load genre names from text files
genres = load_genres()

## 2. Generate image directories for each genre if it doesn't exist already
generate_directories(genres)

## 3. Map each genre to a list of artists associated with that genre
## Time: 1 - 5 minutes
genresToArtists = generate_dictionary(genres)

## 4. Write this mapping to a text file
write_genre_artist_map(genresToArtists)

## 5. Read from text file which maps genres to artists and download collection of album art for each artist,
## placing images in their respective image directory
## Time: 5 - 10 hours
download_album_art()
