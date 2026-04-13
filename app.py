import streamlit as st
import os
from dotenv import load_dotenv
from MusicMoodSelector import get_spotify_client, get_all_tracks, analyse_tag, get_target_mood_tracks, create_playlist, mood_map

#map for images to match mood
mood_images = {
    "happy" : "assets/FigureHappy.png",
    "sad" : "assets/FigureSad.png",
    "chill" : "assets/FigureChill.png",
    "gym" : "assets/FigureGym.png"
}
default_image = "assets/FigureNeutral.png"

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
            
    /* prevent blurs */
    /* Remove the border and center the image */
    img {
        image-rendering: pixelated !important;
        border: none !important; /* Removes the border */
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Ensure the container for the image is centered */
    div[data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }
            
    /* Target the button via its data-testid */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* Target the button container inside the header */
    div[data-testid="stHeader"] button {
        display: none !important;
    }

    /* This one hides the actual text content of the button */
    [data-testid="stSidebarCollapseButton"] > span {
        display: none !important;
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
c.write("Choose your desired mood with Mimi")

#displaying figure

#sidebar to reset figure
with st.sidebar:
    st.header("Settings")

    #reset button
    if st.button("Reset Mimi"):
        st.session_state.selected_mood = None
        st.rerun()

image_to_show = mood_images.get(st.session_state.selected_mood, default_image)

col1, col2, col3 = st.columns([1.5, 2, 1])
with col2:
    st.image(image_to_show, width = 250)

#displaying mood buttons
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

try:
    api_key = st.secrets.get("API_KEY") 
except:
    api_key = os.getenv("API_KEY")

# interaction Logic
if st.button("Generate Playlist", type="primary"):
    if not playlist_url or not api_key:
        st.error("Missing Playlist URL or API Key.")
    elif not st.session_state.selected_mood:
        st.error("Please select your desired mood first!")
    else:
        target_mood = st.session_state.selected_mood
        with st.spinner("One second, making your playlist..."):
            try:
                # Logic 
                sp = get_spotify_client()
                tracks = get_all_tracks(sp, playlist_url)

                #check if tracks is None
                if tracks is None:
                    st.error("Could not fetch playlist. Please check your URL or API keys.")
                else:
                    filtered = get_target_mood_tracks(api_key, tracks, target_mood)
                    
                    if filtered:
                        new_url = create_playlist(sp, filtered, target_mood, playlist_url)
                        st.success("Playlist created successfully!")
                        st.link_button("Open Playlist", new_url)
                    else:
                        st.info("No tracks matched that mood.")
            except Exception as e:
                st.error(f"Error: {e}")

