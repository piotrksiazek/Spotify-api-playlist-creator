# Spotify playlist creator

> Live version https://spotipycreator.herokuapp.com/

## Functionality

When logged in with Spoitfy you will be able to access functionalities. First step is to go to My Items tab and make a new playlist.
Then you can choose one of following:

* Mirror Playlist - select origin playlist that belongs to your personal Spotify account and select one of created playlists (theese are hosted on
my account but you are the only one that can modify them). After submitting, destination playlist will contain the same amount of songs and
matching artists, but with different tracks. For example if you have:
```
Stairway to heaven - Led Zeppelin
Little wing - Jimi Hendrix
```
The final playlist may look like:

```
No Quarter - Led Zeppelin
Purple Haze - Jimi Hendrix
```

* One track for one album - pretty self explanatory. You enter spotify artist id, select destination playlist and you get one track from each album.

* All about that track - enter spotify track ID and you will see pretty interesting information normally hidden by spotify, like audio characteristics.
You will also see discography with descriptions, lyrics, artist bio and a little playback addon. Note that obscure tracks may not return lyrics etc.

* Least popular track - enter spotify artist ID and you will get the least popular track from that artist. Popularity isn't based fully on number of views,
so the least popular track in spotify's sense may be not the least viewed.

* Custom recommendations - choose origin (from which you will take your seed) and destination playlist. Then select at most 5 songs and genres
and depth of search and server will find recommendations based on recommendations basend on recommendations etc. based on the depth you
have chosen.
