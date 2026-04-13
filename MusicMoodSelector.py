import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import os
from dotenv import load_dotenv 
import streamlit as st

load_dotenv()

mood_map = {
    "happy" : ["happy", "cheerful", "upbeat", "feel good", "joyful", "positive"],
    "sad": ["yearning", "sad", "depressed", "melancholy", "heartbreak", "gloomy"],
    "chill": ["chill", "mellow", "relaxed", "calm", "ambient", "lo-fi"],
    "gym": ["gym", "party", "dance", "club", "high energy", "electronic"]
}

new_playlist = []

def get_spotify_client():
    # Use st.secrets if available else fallback to os.getenv
    client_id = st.secrets.get("CLIENT_ID") or os.getenv("CLIENT_ID")
    client_secret = st.secrets.get("CLIENT_SECRET") or os.getenv("CLIENT_SECRET")
    redirect_uri = st.secrets.get("REDIRECT_URI") or os.getenv("REDIRECT_URI")
    scope = st.secrets.get("SCOPE") or os.getenv("SCOPE")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    ))
    return sp

def get_all_tracks(sp, playlist_id):
    all_tracks = []
    fields = "items(track(uri, name, artists)), next"
    #get all items
    try:
        #use Spotify's API to get playlist data
        results = sp.playlist_tracks(playlist_id, fields = fields)
    except Exception as e:
        print("Invalid playlist ID/link please try again.")
        return None 
    
    #while there is still a next page
    while results:
        for item in results['items']:
            if item['track'] and item['track']['uri']:
                all_tracks.append((item['track']['uri'], item['track']['name'], item['track']['artists']))
        
        if results['next'] is None:
            results = None
        else:
            results = sp.next(results)
    return all_tracks

#figures out if track matches provided mood, if it does, return true else false
def analyse_tag(api_key, name, artists, target_mood):
    #handle for when artists could be a list
    if isinstance(artists, list):
        artist = artists[0]['name']
    else:
        artist = artists

    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method" : "track.getTopTags",
        "artist" : artist,
        "track" : name,
        "api_key" : api_key,
        "format" : "json"
    }

    #make request and get success response
    try:
        response = requests.get(base_url, params = params, timeout = 5)

        #if request was successful
        if response.status_code == 200:
            data = response.json()

            #get list of dictionary of all tags
            top_tags_list = data.get("toptags", {}).get("tag", [])
            
            if top_tags_list == []:
                return False

            all_tags_list = []
            for this_dict in top_tags_list:
                all_tags_list.append(this_dict["name"].lower())
        else:
            return False 

        #check any tags in all_tags_list match target_mood
        for this_tag in all_tags_list:
            if this_tag.lower() in mood_map[target_mood]:
                return True 
        return False
    except Exception as e:
        print(f"Error occured when requesting life.fm tags: {e}")
        return False 
    
def get_target_mood_tracks(api_key, all_tracks, target_mood):
    target_mood_tracks = []

    #loop through all tracks in provided playlist
    for this_track in all_tracks:
        this_name = this_track[1]
        this_artist = this_track[2]

        #call analyse_tag to see if it matched the target mood
        if analyse_tag(api_key, this_name, this_artist, target_mood):
            #add to list of tracks which match target mood
            target_mood_tracks.append(this_track)
    
    return target_mood_tracks

def create_playlist(sp, target_mood_tracks, target_mood, original_playlist_id):
    #extract all uris
    track_uris = [uri for uri, name, artists in target_mood_tracks]

    #get current user's id for playlist creation
    current_user_id = sp.current_user()['id']

    #create playlist
    new_playlist_name = f"{sp.playlist(original_playlist_id)['name']} - {target_mood} mood"
    playlist_title = target_mood[0].upper() + target_mood[1:]
    description = f"{playlist_title} mood playlist made by Music Mood Selector."

    #create new playlist using Spotify's API
    new_playlist = sp.user_playlist_create(
        user = current_user_id,
        name = new_playlist_name,
        public = False,
        description = description
    )

    #add all tracks which match the mood to newly created playlist 
    if track_uris:
        sp.playlist_add_items(new_playlist['id'], track_uris)
    
    return new_playlist['external_urls']['spotify']

#calling functions to test functionality in terminal
def main():
    sp = get_spotify_client()
    lastfm_api_key = os.getenv("API_KEY")

    #validate input playlist ID/Link
    valid_playlist_input = False
    while not valid_playlist_input:
        playlist_input = input("Enter your playlist link/playlistID: ")

        if "playlist/" in playlist_input:
            playlist_input = playlist_input.split("playlist/")[1].split("?")[0]
        
        all_tracks = get_all_tracks(sp, playlist_input)
        if all_tracks is not None:
            valid_playlist_input = True

    #validate input target mood
    valid_target_mood = False
    while not valid_target_mood:
        target_mood = input("Choose one of the available moods: 'happy', 'sad', 'chill', 'gym'\nYour mood: ")

        if target_mood.lower() in mood_map:
            valid_target_mood = True
        else:
            print("Invalid mood. Please try again.")
        
    target_mood_tracks = get_target_mood_tracks(lastfm_api_key, all_tracks, target_mood)

    #if list of tracks which match target mood is empty exit 
    if not target_mood_tracks:
        print(f"Sorry, no songs in this playlist matched the '{target_mood}' mood.")
        return 
    else:
        new_playlist_url = create_playlist(sp, target_mood_tracks, target_mood, playlist_input)
        print(f"Successfully created new playlist: {new_playlist_url}")

    return new_playlist_url

if __name__ == "__main__":
    main()

