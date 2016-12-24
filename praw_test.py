import praw
import re
import pprint as pp
import spotipy
from difflib import SequenceMatcher

spot = spotipy.Spotify()

def main():
    fp = open("required_spotbot","r")
    info = fp.read().split()
    fp.close()
    user_agent = info[0]
    client_id = info[1]
    client_secret = info[2]
    password = info[3]
    username = info[4]
    r = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent,
                    username=username,
                    password=password)
    domains = ['youtube.com','m.youtube.com','youtu.be']
    r_spotmebot = r.subreddit('spotmebot')
    for i,s in enumerate(r_spotmebot.stream.submissions()):

        if s.domain in domains:
            if s.media and s.media['oembed'] and s.media['oembed']['title']:
                media_title = s.media['oembed']['title']
                submission_title = s.title
                # print("+\t",submission_title)
                if '-' in media_title and '-' in submission_title:
                    results,via = getSpotifyURL(media_title,submission_title)
                    if results:
                        reply_text = "[Spotify Link]("+results+")\nfound via "+str(via)
                        s.reply(reply_text)
                    else:
                        continue
            else:
                print("== didnt make the cut ==")


def getSpotifyURL(media_title,submission_title):
    # print("Original:\t",media_title)
    media_artist,media_song = parseTitle(media_title)
    submission_artist,submission_song = parseTitle(submission_title)
    # print("Media:\t\t",media_artist,"-",media_song)
    # print("Post:\t\t",submission_artist,"-",submission_song)

    a,s,url = findByTitle(submission_artist,submission_song)
    if url:
        return url,1
    # print("\tcheck media title")
    media_best_match,media_ratio,media_best_url = findByArtist(media_artist,media_song)
    # print("\tcheck submission title")
    submission_best_match,submission_ratio,submission_best_url = findByArtist(submission_artist,submission_song)



    if media_best_match and submission_best_match:
        close_match_ratio = SequenceMatcher(None, media_best_match, submission_best_match).ratio()
        if close_match_ratio >= 0.85 and (media_ratio+submission_ratio) >= 1.5:
            print(media_best_match,"(",media_ratio,")","\t==\t",submission_best_match,"(",submission_ratio,")")
            return media_best_url,2
        else:
            print(media_best_match,"(",media_ratio,")","\t=/=\t",submission_best_match,"(",submission_ratio,")")
            return False,0
    return False,0

def findByTitle(in_artist,in_song):
    song_results = spot.search(q=in_song, type='track',limit=50)
    for song in song_results['tracks']['items']:
        artist = song['artists'][0]['name'].lower()
        # pp.pprint(song)
        url = song['external_urls']['spotify']
        # print("----")
        # print(artist,"=?=",in_artist)
        # print("----")
        ratio = SequenceMatcher(None, in_artist, artist).ratio()
        if ratio > 0.7:
            # print("[FOUND]\t",artist,"-",song['name'],"(",ratio,")")
            return artist,song,url
    return None,None,None
    # pp.pprint(song_results)


def findByArtist(in_artist,in_song):
    artist_results = spot.search(q=in_artist, type='artist')

    artist_uri = None
    if artist_results['artists']['items']:
        artist_uri = artist_results['artists']['items'][0]['uri'] 
    #TODO check top 4 artists (if needed)

    if not artist_uri:
        return None,None,None

    tracks = []
    track_names = []

    albums = spot.artist_albums(artist_uri,album_type='album',limit=50)

    for album in albums['items']:
        album_tracks = spot.album_tracks(album['uri'],limit=50)
        # print(album['name'])
        for track in album_tracks['items']:
            tracks.append(track)
            track_names.append(track['name'].lower())

    best_ratio = 0
    best_index = -1
    for index,song in enumerate(track_names):
        ratio = SequenceMatcher(None, in_song, song).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_index = index
    if best_index != -1:
        best_url = tracks[best_index]['external_urls']['spotify']
        return track_names[best_index],best_ratio,best_url
    else:
        return None,None,None

def parseTitle(title):
    splitted = title.split('-')
    artist_name = splitted[0]
    song_name = splitted[1]
    artist_name = re.sub(r'([\(\{\[]).*([\)\}\]])','',artist_name)
    artist_name = re.sub(r'[\"\'"]','',artist_name)
    song_name = re.sub(r'([\(\{\[]).*([\)\}\]])*','',song_name)
    song_name = re.sub(r'[\"\'"]','',song_name)
    return artist_name.strip().lower(),song_name.strip().lower()


if __name__ == '__main__':
    main()