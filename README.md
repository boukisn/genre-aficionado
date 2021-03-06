# Genre Aficionado
An ongoing project by Nick Boukis to visualize and find trends in music. My main goal is to use machine learning to identify genres based on album covers. I have also created the [Chromatic Genre Explorer](http://boukisn.github.io/genre-aficionado/chroma/) which breaks down genres by color and maps them in 3D space.
Utilizes Spotify's [Web API](https://developer.spotify.com/web-api/) & Google's [TensorFlow](https://www.tensorflow.org/).

### Getting Album Art (Option 1, Quick, Easy)
1. Run `wget https://www.dropbox.com/s/m8sidpj5pekp6qm/genre_images.zip?dl=1 -O genre_images.zip` from within the repository.
2. Unzip the contents of `genre_images.zip`.

### Getting Album Art (Option 2, Up-to-Date, Customizable)
1. Update `genres.txt` with your list of genres separated by newlines (No need to edit `genres_to_artists.txt` as this will be updated automatically).
2. Run `python spotify_load.py` (_Note: This may take up to 5-6 hours if you use every genre_).

### Training Images
_Coming soon!_