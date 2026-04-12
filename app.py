import streamlit as st
import os
from dotenv import load_dotenv
from MusicMoodSelector import get_spotify_client, get_all_tracks, analyse_tag, get_target_mood_tracks, create_playlist, mood_map

st.set_page_config(page_title="Music Mood Selector", layout = "centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Force the font on every text */
    * {
        font-family: 'Press Start 2P', cursive !important;
    }

    /* Fix the Title specifically */
    h1 {
        font-family: 'Press Start 2P', cursive !important;
        font-size: 32px !important; /* Pixel fonts are big, keep this reasonable */
    }

    /* Fix paragraph text */
    p, div, label {
        font-family: 'Press Start 2P', cursive !important;
        font-size: 12px !important;
    }

    /* Fix Buttons */
    div.stButton > button {
        font-family: 'Press Start 2P', cursive !important;
        font-size: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

load_dotenv()

st.title("Music Mood Selector")
st.markdown("Create a new playlist of your desired mood based on your Spotify playlist!")

if 'selected_mood' not in st.session_state:
    st.session_state.selected_mood = None

playlist_url = st.text_input("Enter your playlist URL/ID")

#create container for moood buttons
c = st.container()
c.write("Choose your desired mood")

mood_button_cols = st.columns(len(mood_map))

for i, mood in enumerate(mood_map.keys()):
    is_selected = (st.session_state.selected_mood == mood)
    if mood_button_cols[i].button(
        mood.capitalize(),
        use_container_width = True,
        type="primary" if is_selected else "secondary"
    ):
        st.session_state.selected_mood = mood
        st.rerun()

api_key = os.getenv("API_KEY")

# Interaction Logic

if st.button("Generate Playlist", type="primary"):
    if not playlist_url or not api_key:
        st.error("Missing Playlist URL or API Key.")
    elif not st.session_state.selected_mood:
        st.error("Please select your desired mood first!")
    else:
        target_mood = st.session_state.selected_mood
        with st.spinner("Analyzing tracks and filtering by mood..."):
            try:
                # Logic 
                sp = get_spotify_client()
                tracks = get_all_tracks(sp, playlist_url)
                filtered = get_target_mood_tracks(api_key, tracks, target_mood)
                
                if filtered:
                    new_url = create_playlist(sp, filtered, target_mood, playlist_url)
                    st.success("Playlist created successfully!")
                    st.link_button("Open Playlist", new_url)
                else:
                    st.info("No tracks matched that mood.")
            except Exception as e:
                st.error(f"Error: {e}")

