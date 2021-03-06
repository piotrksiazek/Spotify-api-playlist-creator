from typing import List
from spotipy import Spotify
import random
from Track import Track

class Playlist:
    """
    Wrapper class for methods related to playlists.
    """
    @staticmethod
    def addPrefixesTo(track_list: List[str]):
        """
        checks if track list items start with spotify:track: and if not, returns mapped list
        """
        return ['spotify:track:' + track_id for track_id in track_list]

    @staticmethod
    def get_playlist_items(spotify: Spotify, playlist_id: str, type_of_item: str, unique: bool) -> List[str]:
        """
        :param spotify: spotipy.Spotify class instance
        :param playlist_id: playlist id
        :param type_of_item: 'artist' if desired items are artists and 'track' if they are tracks
        :param unique: if True returned list is unique, if False list can contain duplicates
        :returns: unique list of artists from playlist or list of all tracks
        """
        playlist = spotify.playlist_items(playlist_id)
        items_from_playlist = []
        if type_of_item == 'artist':
            for index, item in enumerate(playlist['items']):
                artist = playlist['items'][index]['track']['album']['artists'][0]['id']
                items_from_playlist.append(artist)
        elif type_of_item == 'track':
            for index, item in enumerate(playlist['items']):
                track = {}
                track['id'] = playlist['items'][index]['track']['id']
                track['name'] = playlist['items'][index]['track']['name']
                items_from_playlist.append(track)

        return list(set(items_from_playlist)) if unique else items_from_playlist

    @staticmethod
    def get_id_of_newest_playlist(spotify: Spotify) -> str:
        """
        :param spotify: spotipy.Spotify class instance
        :returns: id of the most recently created playlist on account
        """
        new_playlist = spotify.current_user_playlists(limit=1, offset=0)
        return new_playlist['items'][0]['id']

    @staticmethod
    def get_corresponding_top_tracks(spotify: Spotify, artists_id_list: List[str], tracks_from_old_playlist: List[str]) -> List[str]:
        """
        :param spotify: spotipy.Spotify class instance
        :param artists_id_list: List of artists' ids
        :param tracks_from_old_playlist: List of tracks' ids from a playlist we we want to base the action on
        :returns: list of found track ids
        """
        track_list = []
        for artist_id in artists_id_list:
            top_tracks = spotify.artist_top_tracks(artist_id, country='PL')['tracks']
            top_tracks_length = len(top_tracks)
            for track_index in range(top_tracks_length):
                track_id = top_tracks[track_index]['id']
                if track_id in tracks_from_old_playlist:
                    continue  # We don't want duplicates
                else:
                    track_list.append(track_id)
                    break  # We want only one corresponding track
        return track_list

    @staticmethod
    def get_non_popular_tracks(spotify: Spotify, artists_id_list: List[str], tracks_from_old_playlist: List[str]) -> List[str]:
        """
        :param spotify: spotipy.Spotify class instance
        :param artists_id_list: List of artists' ids
        :param tracks_from_old_playlist: List of tracks' ids from a playlist we we want to base the action on
        :returns: list of corresponding track ids that are not listed in top artist's songs, chosen randomly
        """
        track_list = []
        for artist_index, artist_id in enumerate(artists_id_list):
            while True:
                try:
                    albums = spotify.artist_albums(artist_id)['items']
                    number_of_albums = len(albums)
                    random_album_index = random.randint(0, number_of_albums - 1)
                    random_album_id = albums[random_album_index]['id']
                    random_album = spotify.album_tracks(random_album_id)['items']
                    number_of_tracks = len(random_album)
                    random_track_index = random.randint(0, number_of_tracks - 1)
                    random_track_id = random_album[random_track_index]['id']
                except ValueError:
                    #just in case empty range for randrange() (0, 0, 0)
                    break

                if random_track_id in tracks_from_old_playlist:  # We didn't find anything new
                    continue
                else:
                    track_list.append(random_track_id)
                    break
        if 'spotify:track:' not in track_list[0]:
            track_list = ['spotify:track:' + track_id for track_id in track_list]
        return track_list

    @staticmethod
    def create_new_playlist(spotify: Spotify, name: str, user: str):
        """
        Just a wrapper around already existing spotipy function. Creates new playlist with a given name.
        :param spotify: spotipy.Spotify class instance
        :param name: name of the playlist to be created
        :param user: spotify user id
        :returns: None
        """
        spotify.user_playlist_create(user=user, name=name)

    @staticmethod
    def get_hipster_tracks(spotify: Spotify, artists_id_list: List[str], tracks_from_old_playlist: List[str]) -> List[str]:
        pass

    @staticmethod
    def is_playlist_name_unique(spotify: Spotify, playlist_name: str, user: str) -> bool:
        """
        :param spotify: spotipy.Spotify class instance
        :param playlist_name: Playlist name in human readable format, not id
        :param user: spotify user id
        :returns: True if playlist name is unique for the user and False if not unique.
        """
        playlists = spotify.user_playlists(user)['items']
        for i in range(len(playlists)):
            if playlists[i]['name'] == playlist_name:
                return False
        return True

    @staticmethod
    def get_playlist_id_with_name(spotify: Spotify, playlist_name: str, user: str) -> str:
        """
        :param spotify: spotipy.Spotify class instance
        :param playlist_name: Playlist name in human readable format, not id
        :param user: spotify user id
        :returns: playlist id corresponding with param playlist_name if found, None if not.
        """
        playlists = spotify.user_playlists(user)['items']
        for i in range(len(playlists)):
            if playlists[i]['name'] == playlist_name:
                return playlists[i]['id']

    @staticmethod
    def get_random_track_from_each_album(spotify: Spotify, artist_id: str, include_singles=False) -> List[str]:
        """
        :param spotify: spotipy.Spotify class instance
        :param artist_id: desired artists id
        :param include_singles: if True albums of type single will be considered, False by default
        :returns: List with one random track id for each album from given artist
        """
        items = spotify.artist_albums(artist_id)['items']
        if include_singles:
            albums_ids = [track['id'] for track in items]
        else:
            albums_ids = [track['id'] for track in items if track['album_type'] != 'single']
        random_track_ids = []
        for album_id in albums_ids:
            random_track_id = Track.get_random_track_id_from_album(spotify, album_id)
            random_track_ids.append(random_track_id)
        return Playlist.addPrefixesTo(list(set(random_track_ids)))

    @staticmethod
    def clear_playlist(spotify: Spotify, playlist_id: str, user: str) -> None:
        """
        Deletes all songs from a playlist but not the playlist itself.
        :param spotify: spotipy.Spotify class instance.
        :param playlist_id: id of playlist to clear. Must be owned by user and hosted on account.
        :param user: spotify user id.
        """
        playlist_items = spotify.playlist_items(playlist_id)['items']
        track_ids = [item['track']['id'] for item in playlist_items]
        spotify.user_playlist_remove_all_occurrences_of_tracks(user, playlist_id, track_ids)

    @staticmethod
    def get_all_track_ids_from_user_playlists(spotify: Spotify, user_id: str):
        """
        :param spotify: spotipy.Spotify class instance.
        :param user_id: id of user.
        :returns List of all tracks of user on public playlists.
        """
        user_playlists_id = [playlist['id'] for playlist in spotify.user_playlists(user_id)['items']]
        all_tracks = []
        for playlist_id in user_playlists_id:
            playlist = spotify.playlist_items(playlist_id)['items']
            for track in playlist:
                all_tracks.append(track['track']['id'])
        return all_tracks

    @staticmethod
    def get_deep_recommendations(spotify: Spotify, user_id: str, seed_tracks: List[str], seed_genres: List[str], min_depth: int, size: int) -> List[str]:
        """
        Searches spotify using recommendations and based on depth parameter, searches for recommendations of recommendations
        so that returned list of tracks isn't directly related to seed tracks. Seed_tracks and seed_genres cant't exceed
        more than 5 elements when added.
        :param spotify.Spotify class instance.
        :param user_id: id of user.
        :param seed_tracks: list of track ids.
        :param seed_genres: list of genres.
        :param min_depth: Amount of iterations before anything can be added to playlist.
        :param size: Output track list size.
        :returns list of tracks to be added to playlist.
        """
        all_user_tracks = Playlist.get_all_track_ids_from_user_playlists(spotify, user_id)

        recommendations = spotify.recommendations(seed_tracks=seed_tracks, seed_genres=seed_genres)['tracks']
        recommendations_ids = [track['id'] for track in recommendations]

        new_seed = []
        new_playlist = []
        counter = 0
        max_iter = 50 + min_depth

        while counter < max_iter:
            for recommendation in recommendations_ids:
                if len(new_seed) == 5 - len(seed_genres):
                    break
                if recommendation not in all_user_tracks:
                    new_seed.append(recommendation)
                    all_user_tracks.append(recommendation)
                    if counter > min_depth:
                        if len(new_playlist) == size:
                            return new_playlist
                        else:
                            new_playlist.append(recommendation)
            recommendations = spotify.recommendations(seed_tracks=new_seed, seed_genres=seed_genres)['tracks']
            recommendations_ids = [track['id'] for track in recommendations]
            new_seed = []
            counter += 1
        return new_playlist

    @staticmethod
    def create_new_playlist_from_not_mentioned_songs(spotify: Spotify, old_playlist_id: str, new_playlist_id: str) -> None:
        """
        Creates spotify playlist where each track in new playlist corresponds to a track from old playlist. Artist remains
        the same - eg. Little Wing by Jimi Hendrix may become Purple Haze but certainly not Stairway to Heaven.
        :param spotify: spotipy.Spotify class instance.
        :param old_playlist_id: id of origin playlist
        :param new_playlist_id: id of destination playlist
        """
        artists_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'artist', unique=True)
        tracks_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'track', unique=False)
        new_track_list = Playlist.get_non_popular_tracks(spotify, artists_from_old_playlist, tracks_from_old_playlist)
        spotify.user_playlist_add_tracks(user=spotify, playlist_id=new_playlist_id, tracks=new_track_list)